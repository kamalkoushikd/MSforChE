class latticeRender {
    constructor(containerId, path, labelText = 'Lattice Model') {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container with ID "${containerId}" not found.`);
            return;
        }

        this.path = path;
        this.labelText = labelText;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(50, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.animate = this.animate.bind(this);

        this.init();
        this.loadGLBModel();
        this.animate();
    }

    init() {
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.container.appendChild(this.renderer.domElement);
        this.renderer.setClearColor(0x0f0f12);

        this.camera.position.set(5, 5, 5);
        this.camera.lookAt(0, 0, 0);

        // Add lights
        const ambientLight = new THREE.AmbientLight(0x404040, 2);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
        directionalLight.position.set(5, 5, 5);
        this.scene.add(ambientLight);
        this.scene.add(directionalLight);

        // Add controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;

        // Add label below the renderer
        this.label = document.createElement('div');
        this.label.textContent = this.labelText;
        this.label.style.textAlign = 'center';
        this.label.style.marginTop = '10px';
        this.label.style.color = 'white';
        this.label.style.fontSize = '16px';
        this.container.appendChild(this.label);

        // Resize listener
        window.addEventListener('resize', this.onWindowResize.bind(this));
    }

    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    loadGLBModel() {
        const loader = new THREE.GLTFLoader();
        
        loader.load(
            this.path,
            (gltf) => {
                const model = gltf.scene;

                // Center the model
                const box = new THREE.Box3().setFromObject(model);
                const center = box.getCenter(new THREE.Vector3());
                model.position.sub(center);
                
                this.scene.add(model);
            },
            null, // No need for a progress callback
            (error) => {
                console.error('An error occurred while loading the GLB model:', error);
            }
        );
    }

    animate() {
        requestAnimationFrame(this.animate);
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}
