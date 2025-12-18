import React, { useState, useEffect } from "react";
import {
  Card,
  CardHeader,
  Typography,
  CardBody,
} from "@material-tailwind/react";
import api from "../../utils/Api";

const BusinessCategory = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);

  const limit = 1000;
  const totalPages = Math.ceil(totalRecords / limit);

  /* ---------------- FETCH DATA ---------------- */
  useEffect(() => {
    fetchData(currentPage);
  }, [currentPage]);

  const fetchData = async (page) => {
    setLoading(true);
    try {
      const response = await api.get(
        `/read_master_input/?page=${page}&limit=${limit}`
      );
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
    <div className="mt-8 mb-8 px-4">
      {/* Title */}
      <Typography
        variant="h4"
        className="text-gray-800 font-semibold mb-4"
      >
        Business Category Data
      </Typography>

      {/* Card */}
      <Card className="border border-gray-200 rounded-xl shadow-sm bg-white overflow-hidden">
        {/* Header */}
        <CardHeader
          floated={false}
          shadow={false}
          className="bg-gray-100 border-b border-gray-300 px-6 py-4"
        >
          <Typography variant="h6" className="text-gray-800 font-semibold">
            Business Category
          </Typography>
        </CardHeader>

        {/* Table */}
        <CardBody className="overflow-x-auto px-0 pt-0 pb-2">
          {loading ? (
            <p className="text-center py-8 text-blue-600 font-medium">
              Loading...
            </p>
          ) : (
            <table className="w-full min-w-[900px] table-auto text-left">
              <thead className="bg-gray-50 sticky top-0 z-10">
                <tr>
                  {[
                    "ID",
                    "Category",
                    "City",
                    "Name",
                    "Area",
                    "Address",
                    "Phone 1",
                    "Phone 2",
                    "URL",
                    "Ratings",
                    "Sub Category",
                    "State",
                    "Country",
                    "Email",
                    "Latitude",
                    "Longitude",
                  ].map((head) => (
                    <th
                      key={head}
                      className="border-b border-gray-200 px-4 py-3"
                    >
                      <Typography
                        variant="small"
                        className="text-[11px] font-semibold uppercase text-gray-600"
                      >
                        {head}
                      </Typography>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {data.length === 0 ? (
                  <tr>
                    <td
                      colSpan={16}
                      className="text-center py-8 text-gray-400"
                    >
                      No data found
                    </td>
                  </tr>
                ) : (
                  data.map((item) => (
                    <tr
                      key={item.id}
                      className="hover:bg-gray-50 transition"
                    >
                      {[
                        item.id,
                        item.category,
                        item.city,
                        item.name,
                        item.area,
                        item.address,
                        item.phone_no_1,
                        item.phone_no_2,
                        item.url,
                        item.ratings,
                        item.sub_category,
                        item.state,
                        item.country,
                        item.email,
                        item.latitude,
                        item.longitude,
                      ].map((value, i) => (
                        <td
                          key={i}
                          className="px-4 py-3 text-sm text-gray-700 whitespace-nowrap"
                        >
                          {value ?? "-"}
                        </td>
                      ))}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </CardBody>
      </Card>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-6 flex-wrap">
          <button
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => p - 1)}
            className="px-4 py-1.5 rounded-lg border text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50"
          >
            Previous
          </button>

          {Array.from({ length: totalPages }, (_, index) => (
            <button
              key={index}
              onClick={() => setCurrentPage(index + 1)}
              className={`px-4 py-1.5 rounded-lg text-sm border ${
                currentPage === index + 1
                  ? "bg-blue-600 text-white border-blue-600"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {index + 1}
            </button>
          ))}

          <button
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => p + 1)}
            className="px-4 py-1.5 rounded-lg border text-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default BusinessCategory;
