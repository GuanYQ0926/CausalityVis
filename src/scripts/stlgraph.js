import * as THREE from 'three'
import OrbitControls from 'three-OrbitControls'
const STLLoader = require('three-stl-loader')(THREE)


export default class STLGraph {
  constructor() {
    this.width = 500
    this.height = 500
    this.filepath = '../../static/model/brain.stl'
    // init
    this.scene = new THREE.Scene()
    this.scene.background = new THREE.Color(0xffffff)
    // light
    this.scene.add(new THREE.HemisphereLight(0x443333, 0x111122))
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.35)
    directionalLight.position.set(0, 10, 100)
    this.scene.add(directionalLight)

    this.camera = new THREE.PerspectiveCamera(45, 1, 0.001, 10000)
    this.camera.position.set(-1, -10, 1)

    this.renderer = new THREE.WebGLRenderer({antialias: true})

    this.controls = new OrbitControls(this.camera, this.renderer.domElement)

    this.animate = this.animate.bind(this)
    this.animate()
    this.resetDimensions()
  }
  initScene() {
    // axis
    const axesHelper = new THREE.AxesHelper(5)
    this.scene.add(axesHelper)
    // load stl model
    const loader = new STLLoader()
    loader.load(this.filepath, geometry => {
      // const material = new THREE.MeshBasicMaterial({color: 0xD2CECE})
      const material = new THREE.MeshPhongMaterial({color: 0xD2CECE, specular: 0x111111, shininess: 100, opacity: 0.2, transparent: true})
      const mesh = new THREE.Mesh(geometry.center(), material)
      mesh.scale.set(0.5, 0.5, 0.5)
      this.scene.add(mesh)
    })
  }
  animate() {
    requestAnimationFrame(this.animate)
    this.controls.update()
    this.renderer.render(this.scene, this.camera)
  }
  resetDimensions() {
    this.camera.aspect = this.width / this.height
    this.camera.updateProjectionMatrix()
    this.renderer.setSize(this.width, this.height)
    this.renderer.setPixelRatio(window.devicePixelRatio || 1)
  }
  resetCamera() {
    this.controls.reset()
  }
  renderScene() {
  }
  get domElement() {
    return this.renderer.domElement
  }
  drawSlice() {
    const geometry = new THREE.PlaneBufferGeometry(5, 5, 32, 32)
    const material = new THREE.MeshBasicMaterial({color: 0xffff00, side: THREE.DoubleSide})
    const plane = new THREE.Mesh(geometry, material)
    // plane.rotation.set(new THREE.Vector3( 0, 0, Math.PI / 2))
    plane.rotation.y = Math.PI / 2
    plane.position.set(0, 0, 0)
    this.scene.add(plane)
  }
}
