import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import * as THREE from 'three'

const DATA = [
  { label: 'Régulière', pct: 47, color: '#C9A84C' },
  { label: 'Occasionnelle', pct: 34, color: '#3B82F6' },
  { label: 'Essayé', pct: 16, color: '#8B5CF6' },
  { label: 'Jamais', pct: 3, color: '#475569' },
]

const INNER_R = 1.1
const OUTER_R = 1.9
const DEPTH = 0.4
const GAP = 0.045

function makeSegmentGeo(startAngle, endAngle) {
  const shape = new THREE.Shape()
  shape.moveTo(Math.cos(startAngle) * OUTER_R, Math.sin(startAngle) * OUTER_R)
  shape.absarc(0, 0, OUTER_R, startAngle, endAngle, false)
  shape.lineTo(Math.cos(endAngle) * INNER_R, Math.sin(endAngle) * INNER_R)
  shape.absarc(0, 0, INNER_R, endAngle, startAngle, true)
  shape.closePath()
  return new THREE.ExtrudeGeometry(shape, { depth: DEPTH, bevelEnabled: false, steps: 1 })
}

function Segment({ startAngle, endAngle, color }) {
  const geo = useMemo(() => makeSegmentGeo(startAngle, endAngle), [startAngle, endAngle])
  return (
    <mesh geometry={geo} position={[0, 0, -DEPTH / 2]}>
      <meshStandardMaterial color={color} metalness={0.35} roughness={0.4} />
    </mesh>
  )
}

function DonutGroup() {
  const ref = useRef()
  useFrame(() => { ref.current.rotation.y += 0.005 })

  const totalUsable = 2 * Math.PI - DATA.length * GAP
  let cursor = 0
  const segs = DATA.map((d) => {
    const span = (d.pct / 100) * totalUsable
    const start = cursor + GAP / 2
    const end = cursor + span + GAP / 2
    cursor += span + GAP
    return { ...d, start, end }
  })

  return (
    <group ref={ref} rotation={[-Math.PI / 7, 0, 0]}>
      {segs.map((s) => (
        <Segment key={s.label} startAngle={s.start} endAngle={s.end} color={s.color} />
      ))}
    </group>
  )
}

export function DonutChart3D() {
  return (
    <Canvas camera={{ position: [0, 2.5, 5], fov: 48 }} dpr={[1, 2]}>
      <color attach="background" args={['#0a0d1a']} />
      <ambientLight intensity={0.5} />
      <pointLight position={[3, 4, 3]} intensity={2} color="#ffffff" />
      <pointLight position={[-2, -2, 2]} intensity={0.8} color="#C9A84C" />
      <pointLight position={[0, 0, -4]} intensity={0.4} color="#3B82F6" />
      <DonutGroup />
      <OrbitControls enableZoom={false} enablePan={false} />
    </Canvas>
  )
}
