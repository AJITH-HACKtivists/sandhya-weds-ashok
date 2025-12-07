import { useEffect, useRef, useState } from "react";
import axios from 'axios';
import toastr from "toastr";
import "toastr/build/toastr.min.css";
import LoadingOverlay from "react-loading-overlay-ts";


const file_ext = ['jpg', 'jpeg', 'png', 'mp4']
const Upload = ()=>{
    const [files, setFiles] = useState({});
    const inputref = useRef(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isDragging, setIsDragging] = useState(false);
    useEffect(()=>{
        console.log(wed.imagesUploadUrl)
    }, [])
   

    const addFiles = (filesToUpload)=>{
        let filesToUpdate = {...files};
        const filesToAdd = Array.from(filesToUpload);
        filesToAdd.forEach(file=>{
          if(!file.type.startsWith("video/") || !file.type.startsWith("image/")){
            filesToUpdate[`${file.name}-${file.size}-${file.type}`] = file
          }
        })
        // inputref.current.value = `${Object.keys(filesToAdd).length} files selected`;
        setFiles(filesToUpdate);
    }

     const handleAddFile = (e)=>{
      addFiles(e.target.files)   
    }

    const isSubmitDisabled = ()=>{
      if(Object.keys(files).length === 0){
        return true;
      }    
      return Object.values(files).some((file)=>{
        return !file.type.startsWith("video/") && !file.type.startsWith("image/")
      })
    }

    const removeFile = (key) =>{
        console.log(key);
        let filesToUpdate = {...files}
        if(Object.hasOwn(filesToUpdate, key)){
            delete filesToUpdate[key]
        }
        setFiles(filesToUpdate);
        
    }

    const handleSubmitClick = async ()=>{
      try{
        setIsLoading(true);
        const formData = new FormData();
        Object.values(files).forEach((file) => {
        formData.append("Images", file);
      });
         const response = await axios.post(wed.imagesUploadUrl,formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      if(response.status === 201){
        setFiles({});
        setIsLoading(false);
        toastr.success("Photo uploaded successfully!");
      }
         console.log(response)
      }  
      catch(error){
        toastr.error("Upload failed!");
        console.log(error);
        setIsLoading(false);
      }
      
    }

    const handleZoneClicked = () =>{
        if(inputref.current){
            inputref.current.click()
        }
    }

    const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      addFiles(e.dataTransfer.files);
      e.dataTransfer.clearData();
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

   return (
    <div className="uploads-div-main">
      <LoaderWrapper active={isLoading}>
        <div className="upload-card">   {/* NEW WRAPPER */}

            <h1>Welcome to Sandhya Weds Ashok Engagement</h1>

            <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                className="drag-and-drop-div"
                onClick={handleZoneClicked}
            >
                <div className="content">
                    <h3>Please Drag and drop photos</h3>
                    <p>Click here</p>
                </div>
            </div>

            <input
                type="file"
                multiple
                onChange={handleAddFile}
                ref={inputref}
                accept="image/*,video/*"
                style={{ display: "none" }}
            />

            <button type="button" disabled={isSubmitDisabled()} onClick={handleSubmitClick}>
                Upload
            </button>

            {Object.keys(files).length > 0 && (
                <div className="preview-div">
                    <p>Preview</p>
                    <div className="outer-div">
                        {Object.values(files).map((file) => {
                            const src = URL.createObjectURL(file);
                            return (
                                <div className="photos-div-main" key={file.name}>
                                    <div className="photo-div">
                                        <img src={src} alt="" />
                                    </div>
                                    <div className="photo-details-div">
                                        <button
  type="button"
  className="remove-btn"
  onClick={() => removeFile(`${file.name}-${file.size}-${file.type}`)}
>
  <svg
    width="18"
    height="18"
    viewBox="0 0 24 24"
    fill="none"
    stroke="white"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <polyline points="3 6 5 6 21 6" />
    <path d="M19 6l-1 14H6L5 6" />
    <path d="M10 11v6" />
    <path d="M14 11v6" />
    <path d="M9 6V4h6v2" />
  </svg>
  <span>Remove</span>
</button>

                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

        </div>
       </LoaderWrapper> 
    </div>
);

}

const LoaderWrapper = ({ active, children }) => {
  return (
    <LoadingOverlay
      active={active}
      spinner
      text="Uploading..."
      styles={{
        overlay: (base) => ({
          ...base,
          background: "rgba(0,0,0,0.4)",
          zIndex: 9999,
        }),
      }}
    >
      {children}
    </LoadingOverlay>
  );
};

export default Upload