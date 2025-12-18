import React, { useState } from "react";
import api from "../../utils/Api";

const CollegeDuniaUploader = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle file selection
  const handleFileChange = (e) => {
    console.log("Selected file:", e.target.files[0]);
    setFile(e.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a CSV file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true); // start loading
      const response = await api.post(
        "/upload_college_dunia_data", 
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("Upload successful:", response.data);
      alert("File uploaded successfully!");
      setFile(null); // clear file after upload
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("File upload failed!");
    } finally {
      setLoading(false); // stop loading
    }
  };

  return (
    <div className="p-6 max-w-md bg-white rounded-lg shadow mt-6">
      <h2 className="text-xl font-bold mb-4">Upload Listing CSV File</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
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

export default CollegeDuniaUploader;
