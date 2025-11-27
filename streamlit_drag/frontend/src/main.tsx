import React from 'react'
import { createRoot } from 'react-dom/client'
import DragCanvas from './DragCanvas'


const root = createRoot(document.getElementById('root')!)


// Streamlit component using window.parent.postMessage for simple integration


root.render(<DragCanvas />)
