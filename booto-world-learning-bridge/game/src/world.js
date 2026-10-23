/* Moteur WebGL natif : véritable géométrie 3D, sans bibliothèque distante. */
(function(root){'use strict';
const C={grass:'#7fd9a4',grass2:'#91e4aa',earth:'#c9b898',path:'#e1cfb2',stone:'#e7dfcf',river:'#5f99ae',clean:'#33bddd',trunk:'#7b614f',tree:'#2f9b77',bark:'#a86c52'};
function rgb(h){if(Array.isArray(h))return h;let v=h.replace('#','');return [parseInt(v.slice(0,2),16)/255,parseInt(v.slice(2,4),16)/255,parseInt(v.slice(4,6),16)/255];}
function matmul(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k];return o;}
function perspective(fovy,aspect,near,far){const f=1/Math.tan(fovy/2),m=new Float32Array(16);m[0]=f/aspect;m[5]=f;m[10]=(far+near)/(near-far);m[11]=-1;m[14]=(2*far*near)/(near-far);return m;}
function lookAt(e,t){let z=[e[0]-t[0],e[1]-t[1],e[2]-t[2]];let l=Math.hypot(...z);z=z.map(v=>v/l);let x=[z[2],0,-z[0]];l=Math.hypot(...x);x=x.map(v=>v/l);let y=[z[1]*x[2]-z[2]*x[1],z[2]*x[0]-z[0]*x[2],z[0]*x[1]-z[1]*x[0]];return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-(x[0]*e[0]+x[1]*e[1]+x[2]*e[2]),-(y[0]*e[0]+y[1]*e[1]+y[2]*e[2]),-(z[0]*e[0]+z[1]*e[1]+z[2]*e[2]),1]);}
class Mesh{
 constructor(){this.v=[];this.c=[];}
 tri(a,b,c,color){let h=rgb(color);const ux=b[0]-a[0],uy=b[1]-a[1],uz=b[2]-a[2],vx=c[0]-a[0],vy=c[1]-a[1],vz=c[2]-a[2];let nx=uy*vz-uz*vy,ny=uz*vx-ux*vz,nz=ux*vy-uy*vx;let ll=Math.hypot(nx,ny,nz)||1;let sun=Math.max(0,(nx*.30+ny*.85+nz*.42)/ll);let shade=.63+sun*.37;for(const p of [a,b,c]){this.v.push(...p);this.c.push(...h.map(q=>Math.min(1,q*shade)));}}
 quad(a,b,c,d,color){this.tri(a,b,c,color);this.tri(a,c,d,color);}
 box(x,y,z,w,h,d,color){let x0=x-w/2,x1=x+w/2,y0=y,y1=y+h,z0=z-d/2,z1=z+d/2;
  this.quad([x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1],color);
  this.quad([x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1],color);
  this.quad([x1,y0,z0],[x0,y0,z0],[x0,y1,z0],[x1,y1,z0],color);
  this.quad([x1,y0,z1],[x1,y0,z0],[x1,y1,z0],[x1,y1,z1],color);
  this.quad([x0,y0,z0],[x0,y0,z1],[x0,y1,z1],[x0,y1,z0],color);
  this.quad([x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1],color);
 }
 cone(x,y,z,r,h,color,sides=8){const top=[x,y+h,z];for(let i=0;i<sides;i++){let a=i/sides*Math.PI*2,b=(i+1)/sides*Math.PI*2;this.tri([x+Math.cos(a)*r,y,z+Math.sin(a)*r],[x+Math.cos(b)*r,y,z+Math.sin(b)*r],top,color)}}
 cylinder(x,y,z,r,h,color,n=9){for(let i=0;i<n;i++){const a=i/n*2*Math.PI,b=(i+1)/n*2*Math.PI;let a0=[x+Math.cos(a)*r,y,z+Math.sin(a)*r],a1=[a0[0],y+h,a0[2]],b0=[x+Math.cos(b)*r,y,z+Math.sin(b)*r],b1=[b0[0],y+h,b0[2]];this.quad(a0,b0,b1,a1,color)} }
 sphere(x,y,z,r,color,lat=5,lon=9,scale=[1,1,1]){for(let i=0;i<lat;i++){let t1=i/lat*Math.PI,t2=(i+1)/lat*Math.PI;for(let j=0;j<lon;j++){let a=j/lon*2*Math.PI,b=(j+1)/lon*2*Math.PI;let pt=(t,p)=>[x+Math.sin(t)*Math.cos(p)*r*scale[0],y+Math.cos(t)*r*scale[1],z+Math.sin(t)*Math.sin(p)*r*scale[2]];this.quad(pt(t1,a),pt(t1,b),pt(t2,b),pt(t2,a),color)}}}
 ring(x,z,r,color){for(let i=0;i<18;i++){let a=i/18*2*Math.PI,b=(i+1)/18*2*Math.PI,ra=r-.14;this.quad([x+Math.cos(a)*r,.052,z+Math.sin(a)*r],[x+Math.cos(b)*r,.052,z+Math.sin(b)*r],[x+Math.cos(b)*ra,.052,z+Math.sin(b)*ra],[x+Math.cos(a)*ra,.052,z+Math.sin(a)*ra],color)}}
}
function tree(m,x,z,r=1.2,col='#399e78'){m.cylinder(x,0,z,.19*r,1.4*r,'#836348');m.sphere(x,2.08*r,z,r,col,5,8,[1,1.05,1]);m.sphere(x-.65*r,1.9*r,z+.18*r,.64*r,'#44b886',4,7);}
function flower(m,x,z,c){m.cylinder(x,0,z,.055,.34,'#248f65',5);m.sphere(x,.4,z,.18,c,3,6);}
function house(m,x,z,color='#f5e7d8',roof='#d88c7b',w=4.5){m.box(x,0,z,w,3.15,3.7,color);m.box(x,1,z+1.93,.88,1.8,.12,'#8f7664');for(let ox of [-1.4,1.4]){m.box(x+ox,1.58,z+1.93,.78,.8,.10,'#71cddd');m.box(x+ox,1.95,z+2.00,.83,.09,.1,'#fff8e8')}m.cone(x,3.1,z,w*.8,2.2,roof,4);m.box(x,3.2,z,w+1,.14,4.2,roof)}
function human(m,x,z,cloth,scale=1){m.cylinder(x,0,z,.35*scale,.75*scale,'#31435b',8);m.box(x,.8*scale,z,.88*scale,1.07*scale,.60*scale,cloth);m.sphere(x,2.18*scale,z,.42*scale,'#e3af89',5,9);m.sphere(x,2.43*scale,z-.09*scale,.43*scale,'#343149',4,8,[1,.32,1]);m.cylinder(x-.56*scale,.83*scale,z,.17*scale,.88*scale,cloth,6);m.cylinder(x+.56*scale,.83*scale,z,.17*scale,.88*scale,cloth,6)}
function worldMesh(world){const m=new Mesh();m.box(0,-.55,0,65,.56,54,'#6bc59f');m.box(0,-.18,0,57,.19,46,'#85d8a3');
  // Roads and squares
  m.box(-1,-.03,-.5,55,.06,3.8,'#d5c5b0');m.box(0,-.023,0,10,.07,10,'#e7dfcb');
  m.box(-12,-.015,-5,3.8,.06,11,'#ded0bb');m.box(-11,-.015,8,3.8,.06,14,'#ded0bb');
  for(let k=-20;k<=21;k+=3)m.box(k,.013,-.5,1,.016,.10,'#ffffff');
  // River wavy surface x=16.6..23.6
  const water=world.riverClean?'#35b9e4':'#8bafb2';
  m.box(17.2,-.12,0,8,.07,47,world.riverClean?'#4cc5ed':'#84b0af');
  for(let z=-22;z<23;z+=2){const x=13.5+Math.sin(z*.3)*.33;
    m.box(x,.07,z,.48,.13,2.2,'#c1b18e');m.box(21.15,.07,z,.51,.13,2.2,'#c1b18e');
    m.box(16.3+Math.sin(z*.4)*.4,-.075,z,1.2,.008,.12,world.riverClean?'#ddfaff':'#d4d9be');}
  if(!world.riverClean){for(let k=0;k<16;k++){let z=-17+(k*7.3)%36;let x=15.4+((k*13)%5);m.box(x,-.045,z,.35,.09,.43,k%2?'#cb6658':'#e5e5de');}}
  // Bridge and river path
  m.box(17.1,.12,-9,9,.47,2.1,'#c9ac87');for(let i=0;i<6;i++){let x=13.2+i*1.55;m.box(x,.62,-9.93,.1,.55,.1,'#fae5cb');m.box(x,.62,-8.07,.1,.55,.1,'#fae5cb')}
  // Town hall and nearby architectural focal point
  house(m,0,-10,'#f3e2c8','#df7e78',7.2);m.box(0,.02,0,5.1,.1,4.7,'#ddd3c0');m.cylinder(0,.11,0,1.3,.43,'#9edee1',16);m.cylinder(0,.55,0,.5,.95,'#eaf9f1',10);m.sphere(0,1.52,0,.38,'#32aeb5',4,8);
  house(m,-21,-12,'#ffead2','#dd99a1',4.6);house(m,-21,-3,'#e0def3','#a382bf',4.6);house(m,-22,8,'#ffe6d0','#e8a279',5.6);house(m,8,-15,'#efe1c8','#7c9fca',5.4);
  // Park patches and perimeter, benches
  m.box(-12.7,-.004,13.9,15,.06,14.4,'#6ccc8b');m.box(-12.7,.018,13.9,13,.035,2.2,'#e9d4ab');
  for(const [x,z] of [[-18,17],[-7.7,18],[-18,10.6],[-7.6,10.2]])tree(m,x,z,1.1,'#3ca97b');
  for(let i=0;i<12;i++)flower(m,-19+i*1.0,7.8,i%2?'#ff97aa':'#fbd577');
  m.box(-8,.12,7,2.1,.25,.75,'#bb8159');m.box(-8,.40,6.7,2.1,.77,.2,'#bb8159');
  if(world.treesPlanted){for(const [x,z] of [[-15,13],[-11.5,17],[-9.8,12],[-14,19]])tree(m,x,z,1.0,'#2fa870');for(let k=0;k<26;k++)flower(m,-17+(k*2.1)%13,10+(k*1.45)%9,k%3===0?'#fa8ab5':'#f9c45f')}
  else{for(const [x,z] of [[-15,13],[-11.5,17],[-9.8,12],[-14,19]]){m.cylinder(x,.01,z,.47,.2,'#907455');m.ring(x,z,.75,'#e5d1ac')}}
  if(world.binsVisible){for(let i=0;i<3;i++){m.box(11+i*.95,.12,8,.75,1.3,.7,['#2d9dc0','#eab84f','#49b886'][i]);m.box(11+i*.95,1.46,8,.88,.18,.8,'#28516c')}}
  // Lanterns and small decorative props
  for(const [x,z] of [[-5,3.5],[5,3.5],[-6,-6],[6,-6],[-21,16],[8,10]]){m.cylinder(x,0,z,.12,3.2,'#3d6478');m.sphere(x,3.4,z,.31,'#fff2b7',4,8)}
  for(let k=0;k<19;k++){let x=-28+((k*13.57)%56),z=-22+((k*7.71)%44);if(Math.abs(x)<6&&Math.abs(z)<6||x>11&&x<24||x>-20&&x<-5&&z>8)continue;tree(m,x,z,.45+(k%4)*.16,'#50af83')}
  return m;
}
function compile(gl,type,src){const s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
function program(gl){const v=`attribute vec3 aPos;attribute vec3 aCol;uniform mat4 uMVP;varying vec3 vColor;varying float vDepth;void main(){vec4 p=uMVP*vec4(aPos,1.0);gl_Position=p;vColor=aCol;vDepth=clamp((p.w-10.0)/85.0,0.0,0.30);}`;const f=`precision mediump float;varying vec3 vColor;varying float vDepth;void main(){gl_FragColor=vec4(mix(vColor,vec3(0.72,0.86,0.9),vDepth),1.0);}`;let p=gl.createProgram();gl.attachShader(p,compile(gl,gl.VERTEX_SHADER,v));gl.attachShader(p,compile(gl,gl.FRAGMENT_SHADER,f));gl.linkProgram(p);if(!gl.getProgramParameter(p,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(p));return p;}
class World3D{
 constructor(canvas){this.canvas=canvas;this.gl=canvas.getContext('webgl',{antialias:true,alpha:false,preserveDrawingBuffer:true})||canvas.getContext('experimental-webgl');if(!this.gl)throw Error('WebGL non disponible');const gl=this.gl;this.prg=program(gl);gl.useProgram(this.prg);this.pos=gl.getAttribLocation(this.prg,'aPos');this.col=gl.getAttribLocation(this.prg,'aCol');this.mvp=gl.getUniformLocation(this.prg,'uMVP');this.buffPos=gl.createBuffer();this.buffCol=gl.createBuffer();this.worldBufferPos=gl.createBuffer();this.worldBufferCol=gl.createBuffer();gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);this.replaceWorld({riverClean:false,binsVisible:false,treesPlanted:false});this.angle=0;}
 replaceWorld(state){const m=worldMesh(state),gl=this.gl;this.geoCount=m.v.length/3;gl.bindBuffer(gl.ARRAY_BUFFER,this.worldBufferPos);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(m.v),gl.STATIC_DRAW);gl.bindBuffer(gl.ARRAY_BUFFER,this.worldBufferCol);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(m.c),gl.STATIC_DRAW);this.state=state;}
 drawGeometry(bp,bc,count){const gl=this.gl;gl.bindBuffer(gl.ARRAY_BUFFER,bp);gl.vertexAttribPointer(this.pos,3,gl.FLOAT,false,0,0);gl.enableVertexAttribArray(this.pos);gl.bindBuffer(gl.ARRAY_BUFFER,bc);gl.vertexAttribPointer(this.col,3,gl.FLOAT,false,0,0);gl.enableVertexAttribArray(this.col);gl.drawArrays(gl.TRIANGLES,0,count);}
 render(px,pz,time=0,reduced=false){const gl=this.gl,canvas=this.canvas;const w=Math.max(1,canvas.clientWidth),h=Math.max(1,canvas.clientHeight),ratio=Math.min(window.devicePixelRatio||1,1.75);if(canvas.width!==Math.round(w*ratio)||canvas.height!==Math.round(h*ratio)){canvas.width=Math.round(w*ratio);canvas.height=Math.round(h*ratio);}gl.viewport(0,0,canvas.width,canvas.height);gl.clearColor(.73,.88,.95,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  const eye=[px+18,25,pz+27],target=[px,0,pz];this.VP=matmul(perspective(.82,canvas.width/canvas.height,.1,180),lookAt(eye,target));gl.useProgram(this.prg);gl.uniformMatrix4fv(this.mvp,false,this.VP);this.drawGeometry(this.worldBufferPos,this.worldBufferCol,this.geoCount);
  let m=new Mesh();human(m,px,pz,'#5b68dc',.95);m.ring(px,pz,1.16,'#ffda84');if(!reduced){m.sphere(px,3.12+(Math.sin(time*.004)*.13),pz,.18,'#ffe9a4',3,6);}
  gl.bindBuffer(gl.ARRAY_BUFFER,this.buffPos);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(m.v),gl.DYNAMIC_DRAW);gl.bindBuffer(gl.ARRAY_BUFFER,this.buffCol);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(m.c),gl.DYNAMIC_DRAW);this.drawGeometry(this.buffPos,this.buffCol,m.v.length/3);}
 project(x,y,z){if(!this.VP)return {x:0,y:0,visible:false};const m=this.VP,X=m[0]*x+m[4]*y+m[8]*z+m[12],Y=m[1]*x+m[5]*y+m[9]*z+m[13],W=m[3]*x+m[7]*y+m[11]*z+m[15];return {x:(X/W*.5+.5)*this.canvas.clientWidth,y:(.5-Y/W*.5)*this.canvas.clientHeight,visible:W>0};}
}
root.BootoWorld3D=World3D;
})(typeof globalThis!=='undefined'?globalThis:this);
