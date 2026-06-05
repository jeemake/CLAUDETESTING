import { useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Html, OrbitControls } from '@react-three/drei'

const TOOLS = [
  { name: 'ChatGPT', count: 26, color: '#10A37F' },
  { name: 'Copilot', count: 13, color: '#0078D4' },
  { name: 'Claude', count: 8, color: '#C9A84C' },
  { name: 'Gemini', count: 7, color: '#4285F4' },
  { name: 'Autres', count: 5, color: '#8B5CF6' },
]

const MAX = 26
const MAX_H = 3.2
const W = 0.65
const SPACING = 1.1

function Bar({ x, height, color, name, count }) {
  const meshRef = useRef()
  return (
    <group position={[x, 0, 0]}>
      <mesh ref={meshRef} position={[0, height / 2, 0]}>
        <boxGeometry args={[W, height, W]} />
        <meshStandardMaterial color={color} metalness={0.3} roughness={0.45} emissive={color} emissiveIntensity={0.08} />
      </mesh>
      <Html position={[0, -0.45, 0]} center>
        <div style={{
          color: '#94A3B8',
          fontSize: '11px',
          fontFamily: 'Inter, sans-serif',
          fontWeight: 600,
          whiteSpace: 'nowrap',
          textAlign: 'center',
          textShadow: '0 1px 4px rgba(0,0,0,0.8)',
          pointerEvents: 'none',
        }}>
          {name}
        </div>
      </Html>
      <Html position={[0, height + 0.28, 0]} center>
        <div style={{
          color: '#FFFFFF',
          fontSize: '15px',
          fontFamily: 'Space Grotesk, sans-serif',
          fontWeight: 700,
          textShadow: '0 1px 6px rgba(0,0,0,0.9)',
          pointerEvents: 'none',
        }}>
          {count}
        </div>
      </Html>
    </group>
  )
}

function Grid() {
  const lines = [0, MAX_H * 0.25, MAX_H * 0.5, MAX_H * 0.75, MAX_H]
  const totalW = (TOOLS.length - 1) * SPACING
  return (
    <>
      {lines.map((y) => (
        <line key={y}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              args={[new Float32Array([
                -totalW / 2 - 0.4, y, 0,
                totalW / 2 + 0.4, y, 0
              ]), 3]}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#1E2842" transparent opacity={0.6} />
        </line>
      ))}
    </>
  )
}

function BarsGroup() {
  const ref = useRef()
  useFrame((s) => {
    ref.current.rotation.y = Math.sin(s.clock.elapsedTime * 0.25) * 0.18
  })

  const total = (TOOLS.length - 1) * SPACING
  return (
    <group ref={ref}>
      <Grid />
      {TOOLS.map((t, i) => (
        <Bar
          key={t.name}
          x={i * SPACING - total / 2}
          height={(t.count / MAX) * MAX_H}
          color={t.color}
          name={t.name}
          count={t.count}
        />
      ))}
      <mesh position={[0, -0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[total + 1.6, 1.4]} />
        <meshStandardMaterial color="#0F1221" transparent opacity={0.8} />
      </mesh>
    </group>
  )
}

export function ToolsChart3D() {
  return (
    <Canvas camera={{ position: [0, 2.2, 6.5], fov: 52 }} dpr={[1, 2]}>
      <color attach="background" args={['#0a0d1a']} />
      <ambientLight intensity={0.4} />
      <pointLight position={[0, 5, 4]} intensity={2} color="#ffffff" />
      <pointLight position={[3, 2, -2]} intensity={0.8} color="#3B82F6" />
      <pointLight position={[-3, 1, 2]} intensity={0.6} color="#C9A84C" />
      <BarsGroup />
      <OrbitControls enableZoom={false} enablePan={false} />
    </Canvas>
  )
}
