import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const selected = acceptedFiles[0];
    setFile(selected);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("http://localhost:8000/easy_meals", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Server response:", data);
      alert("Upload successful!");
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed");
    }
  };

  return (
    <>
      <h2>Upload your fridge image</h2>

      <div
        {...getRootProps()}
        style={{
          border: "2px dashed #aaa",
          padding: "20px",
          textAlign: "center",
          cursor: "pointer",
        }}
      >
        <input {...getInputProps()} />
        {isDragActive
          ? "Drop the image here…"
          : "Drag & drop an image here, or click to select"}
      </div>

      {file && (
        <>
          <p>
            Selected file: <strong>{file.name}</strong>
          </p>
          <button onClick={handleUpload}>Send to Backend</button>
        </>
      )}
    </>
  );
}
