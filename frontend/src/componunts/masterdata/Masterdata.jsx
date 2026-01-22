import React, { useState, useEffect } from "react";
import ReusableTable from "../Table/ReusableTable"; 
import api from "../../utils/Api";

const MasterData = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");

  const limit = 1000;
  const totalPages = Math.ceil(totalRecords / limit);

  // 1. DEFINE COLUMNS ONCE (Easy to reorder or hide)
  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Category", accessor: "category" },
    { header: "City", accessor: "city" },
    { header: "Name", accessor: "name" },
    { header: "Area", accessor: "area" },
    { header: "Address", accessor: "address" },
    { header: "Phone 1", accessor: "phone_no_1" },
    { header: "Phone 2", accessor: "phone_no_2" },
    { header: "URL", accessor: "url" },
    { header: "Ratings", accessor: "ratings" },
    { header: "Sub Category", accessor: "sub_category" },
    { header: "State", accessor: "state" },
    { header: "Country", accessor: "country" },
    { header: "Email", accessor: "email" },
    { header: "Lat", accessor: "latitude" },
    { header: "Long", accessor: "longitude" },
    { header: "Reviews", accessor: "reviews" },
    { header: "Facebook", accessor: "facebook_url" },
    { header: "LinkedIn", accessor: "linkedin_url" },
    { header: "Twitter", accessor: "twitter_url" },
    { header: "Description", accessor: "description" },
    { header: "Pincode", accessor: "pincode" },
    { header: "Virtual Phone", accessor: "virtual_phone" },
    { header: "WhatsApp", accessor: "whatsapp_no" },
    { header: "Phone 3", accessor: "phone_no_3" },
    { header: "Avg Spent", accessor: "avg_spent" },
    { header: "Cost for Two", accessor: "cost_for_two" },
  ];

  useEffect(() => {
    fetchData(currentPage, search);
  }, [currentPage, search]);

  const fetchData = async (page, searchTerm = "") => {
    setLoading(true);
    try {
      const response = await api.get(
        `/read_master_input/?page=${page}&limit=${limit}&search=${searchTerm}`
      );
   
      // If 'api.get' returns the JSON directly, remove the .json() line below.
      const result = await response.json(); 
      setData(result.data || []);
      setTotalRecords(result.total_records || 0);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto my-8 px-4">
      {/* HEADER & SEARCH */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Master Data</h2>
        <input
          type="text"
          className="border rounded-lg px-3 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Search..."
          value={search}
          onChange={(e) => {
            setCurrentPage(1);
            setSearch(e.target.value);
          }}
        />
      </div>

      {/* TABLE AREA */}
      <div className="bg-white shadow rounded-lg p-4">
        {loading ? (
          <p className="text-center text-blue-500 font-semibold">Loading data...</p>
        ) : (
          <>
            {/* 2. USE THE COMPONENT (Replaces 50 lines of HTML) */}
            <ReusableTable columns={columns} data={data} />

            {/* PAGINATION CONTROLS */}
            <div className="flex justify-center items-center mt-6 gap-2 flex-wrap">
              <button
                className="px-3 py-1 rounded bg-blue-500 text-white disabled:bg-gray-300"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage((p) => p - 1)}
              >
                Previous
              </button>
              
              <span className="text-sm text-gray-600">
                 Page {currentPage} of {totalPages}
              </span>

              <button
                className="px-3 py-1 rounded bg-blue-500 text-white disabled:bg-gray-300"
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage((p) => p + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default MasterData;