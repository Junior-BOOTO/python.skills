"""Bounded public HTTPS collection; no credentials, redirects or private networks."""
from datetime import datetime, timezone
import hashlib
import http.client
import ipaddress
import json
import socket
import ssl
import time
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
import pandas as pd
from .ingestion import DataError, MAX_BYTES, MAX_ROWS, read_upload, validate_frame


def public_endpoint(url):
    try:
        parts = urlsplit(url)
        if parts.scheme != 'https' or not parts.hostname or parts.port not in (None, 443):
            raise ValueError()
        if parts.username or parts.password or parts.fragment:
            raise ValueError()
        if any(any(word in key.lower() for word in ('token', 'secret', 'password', 'api_key', 'apikey', 'authorization', 'signature')) for key, _ in parse_qsl(parts.query)):
            raise ValueError()
        if any(ord(c) < 32 for c in url) or len(url) > 2048:
            raise ValueError()
        host = parts.hostname.encode('idna').decode('ascii')
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not addresses or any((not ipaddress.ip_address(item[4][0]).is_global or ipaddress.ip_address(item[4][0]).is_multicast or ipaddress.ip_address(item[4][0]).is_reserved) for item in addresses):
            raise ValueError()
        return parts, host, addresses[0][4][0]
    except (ValueError, OSError, UnicodeError) as exc:
        raise DataError('Utilisez une URL HTTPS publique sans identifiants, clé secrète ni réseau privé (port 443).') from exc


class _PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, address):
        super().__init__(host, timeout=10, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        # Connect to the validated IP, keeping hostname verification and SNI.
        raw = socket.create_connection((self.address, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


def fetch_public(url, limit=MAX_BYTES):
    parts, host, address = public_endpoint(url)
    connection = _PinnedHTTPS(host, address)
    started = time.monotonic()
    try:
        path = urlunsplit(('', '', parts.path or '/', parts.query, ''))
        connection.request('GET', path, headers={'Accept': 'application/json,text/csv', 'Accept-Encoding': 'identity', 'User-Agent': 'BOOTO-AutoData/1.0'})
        response = connection.getresponse()
        if response.status != 200:
            raise DataError(f'La source répond HTTP {response.status}. Les redirections ne sont pas suivies ; utilisez le lien final direct.')
        if response.getheader('Content-Encoding', 'identity').lower() != 'identity':
            raise DataError('Réponse compressée non prise en charge ; utilisez une source directe non compressée.')
        chunks, size = [], 0
        while True:
            if time.monotonic() - started > 25:
                raise DataError('La source met trop de temps à répondre. Réessayez avec un jeu de données plus petit.')
            chunk = response.read1(min(65536, limit + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > limit:
                raise DataError('La collecte dépasse la limite totale de 5 Mo.')
        return b''.join(chunks)
    except DataError:
        raise
    except (OSError, http.client.HTTPException, ValueError) as exc:
        raise DataError('Collecte impossible : vérifiez la source, sa disponibilité et son certificat HTTPS.') from exc
    finally:
        connection.close()


def json_table(raw, records_path=''):
    try:
        data = json.loads(raw)
        if records_path:
            for key in records_path.split('.'):
                data = data[key]
        if isinstance(data, list) and data and all(isinstance(row, dict) for row in data):
            # Flatten object fields; list-valued cells are deliberately rejected below.
            frame = pd.json_normalize(data)
        elif isinstance(data, dict) and data and all(isinstance(v, list) for v in data.values()):
            frame = pd.DataFrame(data)
        else:
            raise ValueError()
        if any(frame[c].map(lambda v: isinstance(v, (dict, list))).any() for c in frame):
            raise ValueError()
        return validate_frame(frame)
    except DataError:
        raise
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        raise DataError('JSON non tabulaire ou chemin incorrect. Indiquez le chemin des observations (exemple : data.results).') from exc


def collect(url, format='json', records_path='', pages=1, page_parameter='', first_page=1):
    if format not in ('json', 'csv') or not 1 <= pages <= 5 or first_page < 0:
        raise DataError('Choisissez JSON ou CSV et entre 1 et 5 pages.')
    if pages > 1 and (not page_parameter or not page_parameter.replace('_', '').isalnum()):
        raise DataError('Indiquez le paramètre de pagination (exemple : page).')
    frames, sources, remaining = [], [], MAX_BYTES
    started = time.monotonic()
    for page in range(first_page, first_page + pages):
        if time.monotonic() - started > 45:
            raise DataError('La collecte complète dépasse 45 secondes ; réduisez le nombre de pages.')
        endpoint = url
        if pages > 1:
            parts = urlsplit(url)
            query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != page_parameter]
            endpoint = urlunsplit(parts._replace(query=urlencode(query + [(page_parameter, str(page))])))
        payload = fetch_public(endpoint, remaining)
        remaining -= len(payload)
        frame = json_table(payload, records_path) if format == 'json' else read_upload(payload, 'collecte.csv')
        if frames and frame.columns.tolist() != frames[0].columns.tolist():
            raise DataError('Les pages ont des colonnes différentes. Collecte interrompue pour éviter une fusion incorrecte.')
        frames.append(frame)
        if sum(len(f) for f in frames) > MAX_ROWS:
            raise DataError('La collecte dépasse 30 000 observations.')
        # Preserve query parameter names, never their potentially sensitive values.
        parts = urlsplit(endpoint)
        source = urlunsplit(parts._replace(query=urlencode([(k, '[masqué]') for k, _ in parse_qsl(parts.query)])))
        sources.append({'url': source, 'request_sha256': hashlib.sha256(endpoint.encode()).hexdigest(), 'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload), 'rows': len(frame)})
    result = validate_frame(pd.concat(frames, ignore_index=True))
    metadata = {'collected_at_utc': datetime.now(timezone.utc).isoformat(), 'format': format, 'records_path': records_path, 'pages_requested': pages, 'first_page': first_page, 'page_parameter': page_parameter, 'sources': sources, 'scope': 'Pages demandées uniquement ; exhaustivité non garantie.'}
    return result, metadata
