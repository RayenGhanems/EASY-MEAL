import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles]);
  }, []);

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const clearAll = () => setFiles([]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: true,
  });

  const handleUpload = async () => {
    if (files.length === 0) return;
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("images", file);
    });

    try {
      const response = await fetch("http://localhost:8000/easy_meals", {
        method: "POST",
        credentials: "include",
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
      <div
        style={{
          padding: "20px",
          textAlign: "center",
          width: "100%",
          height: "100%",
        }}
      >
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
            ? "Drop the images here  …"
            : "Drag & drop some images here, or click to select"}
        </div>

        {files.length > 0 && (
          <>
            <p>
              Selected files: <strong>{files.length}</strong>
            </p>
            <ul style={{ listStyle: "none", padding: 0 }}>
              {files.map((f, idx) => (
                <li key={`${f.name}-${f.lastModified}-${idx}`}>
                  {f.name}{" "}
                  <button type="button" onClick={() => removeFile(idx)}>
                    Remove
                  </button>
                </li>
              ))}
            </ul>
            <button onClick={handleUpload}>Send</button>{" "}
            <button type="button" onClick={clearAll}>
              Clear
            </button>
          </>
        )}
      </div>
      <div>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            border: "1px solid black",
            borderBlockColor: "#aaa",
          }}
        >
          <tr>
            <th>Ingredient</th>
            <th>Quantity</th>
          </tr>
        </table>
      </div>
    </>
  );
}
