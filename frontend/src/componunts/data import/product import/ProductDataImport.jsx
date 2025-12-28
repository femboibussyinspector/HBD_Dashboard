import React, { useState } from "react";
import api from "../../../utils/Api";
import { Alert } from "@material-tailwind/react";

const MAX_FILE_SIZE = 30 * 1024 * 1024; // 30MB

const ProductDataImport = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);

  // Handle file selection
  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);

    // Validate file size & type
    const validFiles = [];
    for (let file of selectedFiles) {
      if (!file.name.endsWith(".csv")) {
        alert(`${file.name} is not a CSV file`);
        continue;
      }
      if (file.size > MAX_FILE_SIZE) {
        alert(`${file.name} exceeds 30MB limit`);
        continue;
      }
      validFiles.push(file);
    }

    setFiles(validFiles);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (files.length === 0) {
      // alert("Please select at least one CSV file!");
      setUploadResult("no-files")
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file); // backend should accept "files"
    });

    try {
      setLoading(true);
      setUploadResult(null);

      const response = await api.post(
        "/product/upload/product-data",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Upload successful:", response.data);
      // alert("Files uploaded successfully!");
      setUploadResult("success");
      setFiles([]);
    } catch (error) {
      console.error("Error uploading files:", error);
      // alert("File upload failed!");
      setUploadResult("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-xlg bg-white rounded-lg shadow mt-6">
      <h2 className="text-xl font-bold mb-4">Upload Listing CSV Files</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          multiple
          onChange={handleFileChange}
          disabled={loading}
          className="mb-4 block w-full border border-gray-300 rounded-lg p-2"
        />

        {files.length > 0 && (
          <ul className="mb-4 text-sm text-gray-700">
            {files.map((file, index) => (
              <li key={index}>
                {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
              </li>
            ))}
          </ul>
        )}

        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded-lg text-white flex items-center justify-center ${loading
            ? "bg-gray-500 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
            }`}
        >
          {loading ? (
            <span className="flex items-center">
              <svg
                className="animate-spin h-5 w-5 mr-2 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8v8H4z"
                ></path>
              </svg>
              Uploading...
            </span>
          ) : (
            "Upload"
          )}
        </button>
        {/* Alert Showing */}
        {
          uploadResult && (
            <Alert
              color={uploadResult === "success" ? "green" :
                uploadResult === "no-files" ? "amber" :
                  "red"
              }
              onClose={() => setUploadResult(null)}
              dismissible
              className="mt-4"
            >
              {uploadResult === "success" && "Files uploaded successfully"}
              {uploadResult === "error" && "File upload failed"}
              {uploadResult === "no-files" && "Please select at least one CSV file!"}
            </Alert>
          )
        }
      </form>
    </div>
  );
};

export default ProductDataImport;
