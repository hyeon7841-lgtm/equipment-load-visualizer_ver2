import React, { useEffect, useState } from 'react'
import Draggable from 'react-draggable'


// Basic protocol: Streamlit will pass 'items' by calling the declared component (in dev server or build)
// For the minimal demo, when used as dev, the Python wrapper points to localhost:3000 and
// the component can read initial arguments from window.location.search or via postMessage.


// To simplify, we'll implement simple UI that expects the parent to post initial items via postMessage


interface Item {
id: number
name: string
x: number
y: number
w: number
h: number
}


const DragCanvas: React.FC = () => {
const [items, setItems] = useState<Item[]>([])


useEffect(() => {
// receive initial items from Streamlit (component API handles this in production)
function handle(e: MessageEvent) {
if (e.data && e.data.type === 'STREAMLIT_ITEMS') {
setItems(e.data.items)
}
}
window.addEventListener('message', handle)
window.parent.postMessage({type: 'REQUEST_ITEMS'}, '*')
return () => window.removeEventListener('message', handle)
}, [])


useEffect(() => {
// send updated items back to Streamlit host
window.parent.postMessage({type: 'UPDATED_ITEMS', items}, '*')
}, [items])


return (
<div style={{width: '100%', height: '700px', background: '#f3f3f3', position: 'relative'}}>
{items.map(it => (
<Draggable
key={it.id}
position={{x: it.x, y: it.y}}
onStop={(e, data) => {
setItems(prev => prev.map(p => p.id === it.id ? {...p, x: data.x, y: data.y} : p))
}}
>
<div style={{width: it.w, height: it.h, border: '2px solid #007bff', background: '#ffffff', padding: 6}}>
<div style={{fontSize: 12, fontWeight: 600}}>{it.name}</div>
<div style={{fontSize: 11}}>{it.w}×{it.h} mm</div>
</div>
</Draggable>
))}
</div>
)
}


export default DragCanvas
