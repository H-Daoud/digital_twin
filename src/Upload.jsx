import React, { useRef } from 'react';

function Upload({ onFileUpload }) {
  const fileInputRef = useRef();

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileUpload(file);
    fileInputRef.current.value = null; // Reset file input for re-uploading
  };

  return (
    <div>
      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,image/*"
        onChange={handleChange}
      />
    </div>
  );
}

export default Upload;
