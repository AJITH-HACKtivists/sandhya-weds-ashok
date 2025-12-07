import React from "react"
import Upload from "./components/Uploads"
import { createRoot } from 'react-dom/client';
import ReactDOM from 'react-dom'

const WeddingPage = () =>{
    return (
        <>
          <Upload/>
        </>
    )
}

  const container = document.getElementById("wedding-root");
  if (container){
    const root = createRoot(container);
    root.render(<WeddingPage />);
  }

  