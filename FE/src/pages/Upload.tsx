import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";

type IngredientRow = {
  ingredient: string;
  quantity: number;
  unit: string;
};

export default function Upload() {
  const [files, setFiles] = useState<File[]>([]);
  const [rows, setRows] = useState<IngredientRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles]);
  }, []);

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const clearAll = () => {
    setFiles([]);
    setRows([]);
    setErrorMsg(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: true,
  });

  const handleUpload = async () => {
    if (files.length === 0) return;

    setLoading(true);
    setErrorMsg(null);

    const formData = new FormData();
    files.forEach((file) => formData.append("images", file));

    try {
      const response = await fetch("http://localhost:8000/easy_meals", {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      console.log("Server response:", data);

      // ---- Normalize backend response into table rows ----
      // Adjust this based on your real backend structure.
      const backendList = Array.isArray(data)
        ? data.flatMap((item) =>
            Array.isArray(item.ingredients) ? item.ingredients : []
          )
        : [];

      console.log("Backend ingredient list:", backendList);

      const normalized: IngredientRow[] = (
        Array.isArray(backendList) ? backendList : []
      ).map((item: any) => ({
        ingredient:
          item.ingredient ?? item.name ?? item.label ?? String(item ?? ""),
        quantity: item.quantity ?? item.qty ?? "",
        unit: item.unit ?? item.uom ?? "",
      }));

      setRows(normalized);
      alert("Upload successful!");
    } catch (err: any) {
      console.error("Upload failed:", err);
      setErrorMsg(err?.message ?? "Upload failed");
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleCellChange = (
    rowIndex: number,
    field: keyof IngredientRow,
    value: string
  ) => {
    setRows((prevRows) =>
      prevRows.map((row, idx) =>
        idx === rowIndex ? { ...row, [field]: value } : row
      )
    );
  };

  const removeRow = (rowIndex: number) => {
    setRows((prevRows) => prevRows.filter((_, idx) => idx !== rowIndex));
  };

  const addRow = () => {
    setRows((prev) => [...prev, { ingredient: "", quantity: 0, unit: "" }]);
  };

  const submitTable = async () => {
    const dict: any = rows.map((r) => ({
      ingredient: r.ingredient,
      quantity: r.quantity.toString() + " " + r.unit,
    }));

    console.log("Submitting table data:", dict);

    try {
      const response = await fetch("http://localhost:8000/verify", {
        method: "POST", // or PUT
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(dict),
      });

      const returned_data = await response.json();
      console.log("returned_data :", returned_data);      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      alert("Saved!");
    } catch (e) {
      console.error(e);
      alert("Save failed");
    }
    
  };

  // --- JSX (your "HTML") that uses the styles object ---
  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.title}>🍽️ Easy Meal</h1>
        <p style={styles.subtitle}>
          Upload your fridge photos and edit ingredients
        </p>
      </header>

      <main style={styles.main}>
        <div style={styles.card}>
          <h2 style={styles.sectionTitle}>Scan your fridge</h2>

          <div
            {...getRootProps()}
            style={{
              ...styles.dropzone,
              ...(isDragActive ? styles.dropzoneActive : {}),
            }}
          >
            <input {...getInputProps()} />
            <div style={{ fontWeight: 700 }}>
              {isDragActive
                ? "Drop the images here…"
                : "Drag & drop images here, or click to select"}
            </div>
            <div style={styles.helperText}>
              Tip: upload 1–3 clear photos for best results.
            </div>
          </div>

          {files.length > 0 && (
            <>
              <div
                style={{ marginTop: 14, color: "#6b7280", fontSize: "0.9rem" }}
              >
                Selected files:{" "}
                <strong style={{ color: "#111827" }}>{files.length}</strong>
              </div>

              <ul style={styles.fileList}>
                {files.map((f, idx) => (
                  <li
                    key={`${f.name}-${f.lastModified}-${idx}`}
                    style={styles.fileItem}
                  >
                    <span style={styles.fileName}>{f.name}</span>
                    <button
                      type="button"
                      style={styles.dangerButton}
                      onClick={() => removeFile(idx)}
                    >
                      Remove
                    </button>
                  </li>
                ))}
              </ul>

              <div style={styles.buttonRow}>
                <button
                  style={styles.primaryButton}
                  onClick={handleUpload}
                  disabled={loading}
                >
                  {loading ? "Sending..." : "Send"}
                </button>

                <button
                  type="button"
                  style={styles.secondaryButton}
                  onClick={clearAll}
                  disabled={loading}
                >
                  Clear
                </button>
              </div>
            </>
          )}

          {errorMsg && <div style={styles.error}>{errorMsg}</div>}

          <div style={styles.divider} />

          <h2 style={styles.sectionTitle}>Ingredients</h2>

          <div style={styles.tableWrap}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Ingredient</th>
                  <th style={styles.th}>Quantity</th>
                  <th style={styles.th}>Unit</th>
                  <th style={styles.th} />
                </tr>
              </thead>

              <tbody>
                {rows.length === 0 ? (
                  <tr>
                    <td style={styles.td} colSpan={4}>
                      <span style={{ color: "#6b7280" }}>
                        No ingredients yet.
                      </span>
                    </td>
                  </tr>
                ) : (
                  rows.map((r, i) => (
                    <tr key={i}>
                      <td style={styles.td}>
                        <input
                          style={styles.input}
                          value={r.ingredient}
                          placeholder="e.g. Tomato"
                          onChange={(e) =>
                            handleCellChange(i, "ingredient", e.target.value)
                          }
                        />
                      </td>

                      <td style={styles.td}>
                        <input
                          style={styles.input}
                          value={r.quantity}
                          placeholder="e.g. 2"
                          onChange={(e) =>
                            handleCellChange(i, "quantity", e.target.value)
                          }
                        />
                      </td>

                      <td style={styles.td}>
                        <select
                          style={styles.select}
                          value={r.unit}
                          onChange={(e) =>
                            handleCellChange(i, "unit", e.target.value)
                          }
                        >
                          {r.unit &&
                            !["Kg", "g", "L", "ml", "pcs"].includes(r.unit) && (
                              <option value={r.unit}>{r.unit}</option>
                            )}
                          <option value="">Select…</option>
                          <option value="Kg">Kg</option>
                          <option value="g">g</option>
                          <option value="L">L</option>
                          <option value="ml">ml</option>
                          <option value="pcs">pcs</option>
                        </select>
                      </td>

                      <td style={styles.td}>
                        <div style={styles.rowActions}>
                          <button
                            type="button"
                            style={styles.dangerButton}
                            onClick={() => removeRow(i)}
                          >
                            Remove
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          <div style={styles.buttonRow}>
            <button
              type="button"
              style={styles.secondaryButton}
              onClick={addRow}
            >
              + Add row
            </button>

            <button
              type="button"
              style={styles.primaryButton}
              onClick={submitTable}
            >
              Submit changes
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
// --- Styles object (paste in the same file, below the component) ---
const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #f8fafc, #eef2f7)",
    display: "flex",
    flexDirection: "column",
  },

  header: {
    padding: "28px 20px 12px",
    textAlign: "center",
  },

  title: {
    fontSize: "2rem",
    margin: 0,
    color: "#111827",
    letterSpacing: "-0.02em",
  },

  subtitle: {
    marginTop: 8,
    fontSize: "1rem",
    color: "#6b7280",
  },

  main: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    padding: 20,
  },

  card: {
    backgroundColor: "#ffffff",
    borderRadius: 16,
    padding: 28,
    width: "100%",
    maxWidth: 880,
    boxShadow: "0 10px 30px rgba(0, 0, 0, 0.08)",
  },

  sectionTitle: {
    fontSize: "1.15rem",
    margin: "0 0 12px 0",
    color: "#111827",
  },

  dropzone: {
    border: "2px dashed #cbd5e1",
    borderRadius: 14,
    padding: "18px 16px",
    textAlign: "center",
    cursor: "pointer",
    background:
      "linear-gradient(135deg, rgba(16,185,129,0.06), rgba(59,130,246,0.06))",
    color: "#111827",
    transition: "transform 0.15s ease, box-shadow 0.15s ease",
  },

  dropzoneActive: {
    boxShadow: "0 10px 24px rgba(16, 185, 129, 0.18)",
    transform: "translateY(-1px)",
  },

  helperText: {
    marginTop: 10,
    fontSize: "0.9rem",
    color: "#6b7280",
  },

  fileList: {
    marginTop: 14,
    padding: 0,
    listStyle: "none",
    display: "grid",
    gap: 8,
  },

  fileItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 12px",
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    background: "#fafafa",
  },

  fileName: {
    color: "#374151",
    fontSize: "0.95rem",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
    maxWidth: 520,
  },

  buttonRow: {
    display: "flex",
    gap: 10,
    marginTop: 14,
    flexWrap: "wrap",
  },

  primaryButton: {
    padding: "12px 14px",
    fontSize: "0.95rem",
    fontWeight: 700,
    borderRadius: 10,
    border: "none",
    cursor: "pointer",
    background: "linear-gradient(135deg, #10b981, #059669)",
    color: "#ffffff",
    boxShadow: "0 10px 20px rgba(16,185,129,0.18)",
    transition: "transform 0.15s ease, box-shadow 0.15s ease",
  },

  secondaryButton: {
    padding: "12px 14px",
    fontSize: "0.95rem",
    fontWeight: 700,
    borderRadius: 10,
    border: "1px solid #e5e7eb",
    cursor: "pointer",
    background: "#ffffff",
    color: "#111827",
    transition: "transform 0.15s ease, box-shadow 0.15s ease",
  },

  dangerButton: {
    padding: "8px 10px",
    fontSize: "0.85rem",
    fontWeight: 700,
    borderRadius: 10,
    border: "1px solid #fee2e2",
    cursor: "pointer",
    background: "#fff1f2",
    color: "#b91c1c",
  },

  divider: {
    height: 1,
    background: "#e5e7eb",
    margin: "22px 0",
  },

  tableWrap: {
    overflowX: "auto",
    border: "1px solid #e5e7eb",
    borderRadius: 14,
  },

  table: {
    width: "100%",
    borderCollapse: "separate",
    borderSpacing: 0,
    minWidth: 640,
  },

  th: {
    textAlign: "left",
    padding: "12px 12px",
    fontSize: "0.85rem",
    color: "#6b7280",
    background: "#f9fafb",
    borderBottom: "1px solid #e5e7eb",
  },

  td: {
    padding: "10px 12px",
    borderBottom: "1px solid #eef2f7",
    verticalAlign: "middle",
  },

  input: {
    width: "100%",
    padding: "10px 10px",
    borderRadius: 10,
    border: "1px solid #e5e7eb",
    background: "#ffffff",
    outline: "none",
    fontSize: "0.95rem",
    color: "#111827",
  },

  select: {
    width: "100%",
    padding: "10px 10px",
    borderRadius: 10,
    border: "1px solid #e5e7eb",
    background: "#ffffff",
    outline: "none",
    fontSize: "0.95rem",
    color: "#111827",
    cursor: "pointer",
  },

  rowActions: {
    display: "flex",
    justifyContent: "flex-end",
  },

  error: {
    marginTop: 12,
    color: "#b91c1c",
    background: "#fff1f2",
    border: "1px solid #fee2e2",
    padding: "10px 12px",
    borderRadius: 12,
    fontSize: "0.9rem",
  },
};
