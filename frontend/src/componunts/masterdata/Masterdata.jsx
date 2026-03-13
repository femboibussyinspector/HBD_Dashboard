import React, { useState, useEffect } from "react";
import ReusableTable from "../Table/ReusableTable";
import api from "../../utils/Api";
import {
  Card,
  CardHeader,
  Typography,
  CardBody,
  Input,
  Button,
  Spinner,
} from "@material-tailwind/react";
import { ArrowPathIcon } from "@heroicons/react/24/solid";

const MasterData = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");

  const limit = 1000;
  const totalPages = Math.ceil(totalRecords / limit);

  // Define columns for master data table
  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Global Business ID", accessor: "global_business_id" },
    { header: "ASIN", accessor: "asin" },
    { header: "IFSC", accessor: "ifsc" },
    { header: "MICR", accessor: "micr" },
    { header: "Business Name", accessor: "business_name" },
    { header: "Branch Code", accessor: "branch_code" },
    { header: "Branch", accessor: "branch" },
    { header: "Business Category", accessor: "business_category" },
    { header: "Business Subcategory", accessor: "business_subcategory" },
    { header: "Price", accessor: "price" },
    { header: "List Price", accessor: "listPrice" },
    { header: "Ratings", accessor: "ratings" },
    { header: "Stars", accessor: "stars" },
    { header: "Email", accessor: "email" },
    { header: "Primary Phone", accessor: "primary_phone" },
    { header: "Secondary Phone", accessor: "secondary_phone" },
    { header: "Other Phones", accessor: "other_phones" },
    { header: "Virtual Phone", accessor: "virtual_phone" },
    { header: "WhatsApp Phone", accessor: "whatsapp_phone" },
    { header: "Website URL", accessor: "website_url" },
    { header: "Is Best Seller", accessor: "isBestSeller" },
    { header: "Bought In Last Month", accessor: "boughtInLastMonth" },
    { header: "Image URL", accessor: "ImgUrl" },
    { header: "Facebook URL", accessor: "facebook_url" },
    { header: "LinkedIn URL", accessor: "linkedin_url" },
    { header: "Twitter URL", accessor: "twitter_url" },
    { header: "Address", accessor: "address" },
    { header: "Area", accessor: "area" },
    { header: "City", accessor: "city" },
    { header: "District", accessor: "district" },
    { header: "State", accessor: "state" },
    { header: "Pincode", accessor: "pincode" },
    { header: "Country", accessor: "country" },
    { header: "Latitude", accessor: "latitude" },
    { header: "Longitude", accessor: "longitude" },
    { header: "Avg Fees", accessor: "avg_fees" },
    { header: "Course Details", accessor: "course_details" },
    { header: "Duration", accessor: "duration" },
    { header: "Requirement", accessor: "requirement" },
    { header: "Avg Spent", accessor: "avg_spent" },
    { header: "Cost for Two", accessor: "cost_for_two" },
    { header: "Reviews", accessor: "reviews" },
    { header: "Description", accessor: "description" },
    { header: "Data Source", accessor: "data_source" },
    { header: "Avg Salary", accessor: "avg_salary" },
    { header: "Admission Req List", accessor: "admission_req_list" },
    { header: "Courses", accessor: "courses" },
    { header: "Created At", accessor: "created_at" },
  ];

  useEffect(() => {
    fetchData(currentPage, search);
  }, [currentPage, search]);

  const fetchData = async (page, searchTerm = "") => {
    setLoading(true);
    try {
      const apiBase = import.meta.env.DEV ? "/api" : (import.meta.env.VITE_API_URL || "");
      const queryParams = new URLSearchParams({
        page: currentPage,
        limit: limit,
        search: search,
      });

      const response = await fetch(`${apiBase}/master_table/list?${queryParams}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token") || ""}`
        }
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          window.location.href = "/auth/sign-in";
          return;
        }
        throw new Error(`Backend failed with status ${response.status}`);
      }

      const result = await response.json();
      
      setData(result.data || []);
      setTotalPages(result.total_pages || 1);
      setTotalRecords(result.total_count || 0);
    } catch (err) {
      console.error("Fetch Error:", err);
      setError("Failed to fetch data from backend.");
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

      <Card className="border border-gray-200 rounded-xl shadow-sm bg-white overflow-hidden">
        <CardBody className="overflow-x-auto p-0">
          {loading ? (
            <div className="flex flex-col justify-center py-20 items-center gap-3">
              <Spinner className="h-10 w-10 text-blue-500" />
              <Typography className="animate-pulse text-gray-600 font-medium">
                Retrieving Records...
              </Typography>
            </div>
          ) : (
            <>
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
        </CardBody>
      </Card>
    </div>
  );
};

export default MasterData;