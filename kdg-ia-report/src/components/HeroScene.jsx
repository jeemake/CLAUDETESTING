import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

function WireIco() {
  const ref = useRef()
  useFrame((s) => {
    ref.current.rotation.y = s.clock.elapsedTime * 0.12
    ref.current.rotation.x = s.clock.elapsedTime * 0.07
  })
  return (
    <mesh ref={ref}>
      <icosahedronGeometry args={[2, 1]} />
      <meshStandardMaterial color="#C9A84C" wireframe emissive="#C9A84C" emissiveIntensity={0.15} />
    </mesh>
  )
}

function Orb({ pos, r, color, speed, phase = 0 }) {
  const ref = useRef()
  useFrame((s) => {
    ref.current.position.y = pos[1] + Math.sin(s.clock.elapsedTime * speed + phase) * 0.4
    ref.current.rotation.y = s.clock.elapsedTime * 0.5
  })
  return (
    <mesh ref={ref} position={pos}>
      <sphereGeometry args={[r, 20, 20]} />
      <meshStandardMaterial color={color} metalness={0.7} roughness={0.2} emissive={color} emissiveIntensity={0.1} />
    </mesh>
  )
}

function Ring() {
  const ref = useRef()
  useFrame((s) => {
    ref.current.rotation.z = s.clock.elapsedTime * 0.06
    ref.current.rotation.x = Math.PI / 2.5 + Math.sin(s.clock.elapsedTime * 0.2) * 0.1
  })
  return (
    <mesh ref={ref} position={[0, 0, 0]}>
      <torusGeometry args={[3.2, 0.025, 8, 80]} />
      <meshStandardMaterial color="#C9A84C" emissive="#C9A84C" emissiveIntensity={0.4} transparent opacity={0.6} />
    </mesh>
  )
}

export function HeroScene() {
  return (
    <Canvas camera={{ position: [0, 0, 7], fov: 55 }} dpr={[1, 2]}>
      <color attach="background" args={['#080A14']} />
      <ambientLight intensity={0.25} />
      <pointLight position={[4, 4, 4]} intensity={1.8} color="#C9A84C" />
      <pointLight position={[-4, -3, 2]} intensity={1} color="#3B82F6" />
      <pointLight position={[0, -4, -2]} intensity={0.6} color="#8B5CF6" />
      <WireIco />
      <Ring />
      <Orb pos={[3.2, 1.5, -0.5]} r={0.35} color="#3B82F6" speed={0.9} phase={0} />
      <Orb pos={[-3, -1.2, -0.3]} r={0.28} color="#8B5CF6" speed={1.2} phase={1.5} />
      <Orb pos={[2.2, -2.2, 0.8]} r={0.22} color="#14B8A6" speed={0.7} phase={3} />
      <Orb pos={[-2.5, 2, 0.4]} r={0.18} color="#C9A84C" speed={1.4} phase={0.8} />
      <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.4} />
    </Canvas>
  )
}
