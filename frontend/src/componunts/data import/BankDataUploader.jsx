import React, { useState } from "react";
import api from "../../utils/Api";

const BankDataUploader = () => {
  const [files, setFiles] = useState([]);   
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files); 
    console.log("Selected files:", selectedFiles);
    setFiles(selectedFiles);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (files.length === 0) {
      alert("Please select at least one CSV file!");
      return;
    }

    const formData = new FormData();

    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      setLoading(true);

      const response = await api.post(
        "/upload_bank_data",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Upload successful:", response.data);
      alert("File(s) uploaded successfully!");
      setFiles([]); 
    } catch (error) {
      console.error("Error uploading files:", error);
      alert("File upload failed!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-md bg-white rounded-lg shadow mt-6">
      <h2 className="text-xl font-bold mb-4">Upload Listing CSV File</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          multiple
          onChange={handleFileChange}
          disabled={loading}
          className="mb-4 block w-full border border-gray-300 rounded-lg p-2"
        />

        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded-lg text-white flex items-center justify-center ${
            loading
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
      </form>
    </div>
  );
};

export default BankDataUploader;
