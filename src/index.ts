import * as THREE from "three"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"
import * as vconlose from "vconsole"
if(process.env.NODE_ENV==="development")
{
    let vConsole = new vconlose();
}
let nxUrl,pxUrl,nyUrl,pyUrl,nzUrl,pzUrl
if(process.env.NODE_ENV==="development")
{
    nxUrl = require('../res/skybox/nx.jpg');
    pxUrl = require('../res/skybox/px.jpg');
    nyUrl = require('../res/skybox/ny.jpg');
    pyUrl = require('../res/skybox/py.jpg');
    nzUrl = require('../res/skybox/nz.jpg');
    pzUrl = require('../res/skybox/pz.jpg');
}
else
{
    var nurl = location.href;
    var regx = /\?(?<t>(?<param>[^ &]+)=(?<value>.*)&?)+$/g;
    nurl.replace(regx,(substring,...arg)=>{
        console.log(substring);
        console.log(arg)
        return '';
    })
    
}

let sphereUrl = require('../res/20190703184417.jpg')
let scene: THREE.Scene = new THREE.Scene();
let camera: THREE.PerspectiveCamera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer: THREE.WebGLRenderer = new THREE.WebGLRenderer();
let control: OrbitControls = new OrbitControls(camera, renderer.domElement);

renderer.setSize(window.innerWidth, window.innerHeight);
function resize()
{
    let h = window.innerHeight;
    let w = window.innerWidth;
    renderer.setSize(w,h);
    camera.aspect = w/h;
    camera.updateProjectionMatrix();
}
function Init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(60,window.innerWidth/window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    resize();
    document.body.appendChild(renderer.domElement);
    (new THREE.CubeTextureLoader).load([pxUrl, nxUrl, pyUrl, nyUrl, pzUrl, nzUrl], texture => {
        scene.background = texture;
    }, Progress => {
        console.log(Progress.loaded);
    }, OnError => {
        console.error(OnError.message);
    })
    //generatorObject();
    SetControls();
    camera.position.set(1, 0, 1);
    camera.lookAt(new THREE.Vector3(0, 0, 0));
}
function setCameraFov(fov:number)
{
    camera.fov = Math.max(Math.min(fov,120),10) 
}
function SetControls() { 
    control = new OrbitControls(camera, renderer.domElement);
    renderer.domElement.addEventListener('wheel', (e: WheelEventEx) => {
        setCameraFov(camera.fov+Math.max(Math.min(e.wheelDeltaY, 1), -1) * -1);
        camera.updateProjectionMatrix();
        console.log(camera.fov);
        e.preventDefault();
        //e.stopPropagation();
    });
    (function(){
        let lastLen = 0;
        function getLen(p1,p2)
        {
            return Math.sqrt(Math.pow(p1.pageX-p2.pageX,2)+ Math.pow(p1.pageY-p2.pageY,2))
        }
        renderer.domElement.addEventListener('touchmove',e=>{
            if(e.touches.length>1)
            {
                let first = e.touches[0];
                let next = e.touches[1];
                let len = getLen(first,next);
                let diff = len - lastLen; 
                let addv = Math.min(Math.max(diff,-1),1)*(Math.abs(diff)/-10);
                setCameraFov(camera.fov+addv);
                lastLen = len;
                camera.updateProjectionMatrix();
                e.preventDefault();
            }
        });
        renderer.domElement.addEventListener('touchstart',e=>{
            if(e.touches.length>1)
            {
                lastLen = getLen(e.touches[0],e.touches[1]);
            }
        });
    })()
    window.addEventListener('resize',resize);
    control.autoRotate = false;
    control.enableZoom = false;
    control.enablePan = false;
}
function generatorObject() {
    let geometry = new THREE.SphereGeometry(100,60,60);
    let material = new THREE.MeshBasicMaterial({ color: 0xffffff,transparent:true,side:THREE.DoubleSide});
    (new THREE.TextureLoader).load(sphereUrl,textrue=>{
        textrue.encoding = THREE.sRGBEncoding;
        material.map = textrue;
        material.needsUpdate = true;
    })
    let cube = new THREE.Mesh(geometry, material);
    scene.add(cube);
}
Init();



function animate() {
    requestAnimationFrame(animate);
    logic();
    renderer.render(scene, camera);

}
function logic() {

}
animate();