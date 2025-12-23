import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

export const citiesList = [
  "Delhi",
  "New Delhi",
  "Gurugram",
  "Noida",
  "Ghaziabad",
  "Faridabad",
  "Chandigarh",
  "Lucknow",
  "Kanpur",
  "Varanasi",
  "Prayagraj",
  "Jaipur",
  "Jodhpur",
  "Udaipur",
  "Kota",
  "Amritsar",
  "Ludhiana",
  "Jalandhar",
  "Srinagar",
  "Jammu",

  "Mumbai",
  "Thane",
  "Navi Mumbai",
  "Pune",
  "Nagpur",
  "Nashik",
  "Aurangabad",
  "Ahmedabad",
  "Surat",
  "Vadodara",
  "Rajkot",
  "Bhavnagar",
  "Jamnagar",
  "Gandhinagar",
  "Indore",
  "Bhopal",

  "Bengaluru",
  "Chennai",
  "Hyderabad",
  "Kochi",
  "Thiruvananthapuram",
  "Coimbatore",
  "Madurai",
  "Mysuru",
  "Vijayawada",
  "Visakhapatnam",
  "Tirupati",


  "Kolkata",
  "Howrah",
  "Bhubaneswar",
  "Cuttack",
  "Ranchi",
  "Patna",
  "Guwahati",
  "Agartala",
  "Shillong",

  "Raipur",
  "Bilaspur",
  "Jabalpur",
  "Gwalior",
  "Dehradun",
  "Haridwar",
  "Rishikesh",
];


import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Spinner,
  Select,
  Option,
} from "@material-tailwind/react";
import {
  MagnifyingGlassIcon,
  ChevronUpDownIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/solid";
import { listingData } from "@/data/listingJSON"; 
import * as XLSX from "xlsx/dist/xlsx.full.min.js";

const defaultColumns = [
  { key: "name", label: "Name", width: 220 },
  { key: "address", label: "Address", width: 320 },
  { key: "website", label: "Website", width: 180 },
  { key: "phone_number", label: "Contact", width: 140 },
  { key: "reviews_count", label: "Review Count", width: 120 },
  { key: "reviews_average", label: "Review Avg", width: 120 },
  { key: "category", label: "Category", width: 140 },
  { key: "city", label: "City", width: 140 },
  { key: "state", label: "State", width: 140 },
];

const convertToCSV = (arr) => {
  if (!arr?.length) return "";
  const headers = Object.keys(arr[0]);
  const rows = arr.map((r) =>
    headers.map((h) => `"${String(r[h] ?? "").replace(/"/g, "'")}"`).join(",")
  );
  return [headers.join(","), ...rows].join("\n");
};

export function cities_reports() {
  const [loading, setLoading] = useState(true);
  const [fullData, setFullData] = useState([]);
  const [pageData, setPageData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;

  const [selectedCity, setSelectedCity] = useState(""); 
  const [categorySearch, setCategorySearch] = useState("");

  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  const [columns] = useState(defaultColumns);
  const selectedCityCount = selectedCity
  ? fullData.filter((x) => x.city === selectedCity).length
  : fullData.length;


  useEffect(() => {
    setLoading(true);
    setTimeout(() => {
      setFullData(listingData);
      setTotal(listingData.length);
      setLoading(false);
    }, 300);
  }, []);

  const uniqueCities = useMemo(() => {
    if (!fullData.length) return [];
    const cities = [...new Set(fullData.map((item) => item.city).filter(Boolean))];
    return cities.sort();
  }, [fullData]);

  const filteredData = useMemo(() => {
    let data = [...fullData];
    const safeValue = (value) => String(value ?? "").toLowerCase();

    if (selectedCity) {
      data = data.filter((x) => safeValue(x.city) === selectedCity.toLowerCase());
    }

    if (categorySearch) {
      const s = categorySearch.toLowerCase();
      data = data.filter((x) => safeValue(x.category).includes(s));
    }

    return data;
  }, [fullData, selectedCity, categorySearch]);

  const sortedData = useMemo(() => {
    if (!sortField) return filteredData;

    return [...filteredData].sort((a, b) => {
      const A = String(a[sortField] ?? "").toLowerCase();
      const B = String(b[sortField] ?? "").toLowerCase();
      if (A === B) return 0;
      return sortOrder === "asc" ? (A > B ? 1 : -1) : (A < B ? 1 : -1);
    });
  }, [filteredData, sortField, sortOrder]);

  useEffect(() => {
    const start = (currentPage - 1) * limit;
    setPageData(sortedData.slice(start, start + limit));
    setTotal(sortedData.length);
  }, [sortedData, currentPage]);

  useEffect(() => {
    setCurrentPage(1);
  }, [selectedCity, categorySearch]);

  const totalPages = Math.max(1, Math.ceil(total / limit));

  const toggleSort = (field) => {
    if (sortField === field) {
      setSortOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  const downloadCSV = (currentOnly = false) => {
    const arr = currentOnly ? pageData : filteredData; 
    const csv = convertToCSV(arr);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = currentOnly ? "cities_report_page.csv" : "cities_report_all.csv";
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadExcel = (currentOnly = false) => {
    const arr = currentOnly ? pageData : filteredData;
    if (!arr.length) return;

    const ws = XLSX.utils.json_to_sheet(arr);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "CitiesData");
    XLSX.writeFile(wb, currentOnly ? "cities_report_page.xlsx" : "cities_report_all.xlsx");
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 rounded bg-[#F8FAFC] text-blue-gray-900">
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
        <div>
          <Typography variant="h4" className="font-bold text-blue-gray-900">
            Cities Data
          </Typography>
          <Typography variant="small" className="font-normal text-gray-500">
            Filter listings by specific cities
          </Typography>
        </div>

        <div className="flex items-center gap-2 flex-wrap justify-end">
          <Button size="sm" onClick={() => downloadCSV(false)} className="bg-gray-900 text-white shadow-none hover:shadow-md">
            CSV All
          </Button>
          <Button size="sm" onClick={() => downloadCSV(true)} variant="outlined" className="border-gray-900 text-gray-900">
            CSV Page
          </Button>
          <Button size="sm" onClick={() => downloadExcel(false)} className="bg-[#607d8b] text-white shadow-none hover:shadow-md">
            Excel All
          </Button>
        </div>
      </div>

      <Card className="h-full w-full border border-gray-200 shadow-sm">
        <div className="flex justify-between flex-col md:flex-row gap-4 items-center m-5">
            <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              <div className="w-full sm:w-72">
                <Select
                  label="Select City"
                  value={selectedCity}
                  onChange={(val) => setSelectedCity(val)}
                  className="bg-white"
                >
                    <Option value="">All Cities</Option>
                    {citiesList.map((city) => (
                      <Option key={city} value={city}>
                        {city}
                      </Option>
                    ))}
                </Select>
              </div>

              <div className="sm:w-72">
                <Input
                  label="Search Category..."
                  value={categorySearch}
                  onChange={(e) => setCategorySearch(e.target.value)}
                  icon={<MagnifyingGlassIcon className="h-5 w-5" />}
                  className="bg-white"
                />
              </div>
            </div>
              <div className="w-55">
                 <div className="border uppercase text-sm bg-white font-semibold text-[#263238] shadow-none hover:shadow-md border-gray-400 rounded-md px-4 py-2 text-[0.950rem]">
                  {
                    selectedCity ? `${selectedCity}: ${selectedCityCount} listings`: `All Cities: ${selectedCityCount} listings`
                  }
                 </div>
                
                
              </div>
        </div>


        <CardBody className="p-0 overflow-x-auto">
          {loading ? (
            <div className="flex justify-center py-20">
              <Spinner className="h-12 w-12 text-gray-900" />
            </div>
          ) : (
            <table className="w-full table-fixed border-collapse min-w-[1200px] text-left">
              <thead className="sticky top-0 z-20 border-b border-gray-200 bg-gray-50 text-xs font-semibold uppercase text-gray-500">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col.key}
                      style={{ width: col.width }}
                      className="px-4 py-3 cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => toggleSort(col.key)}
                    >
                      <div className="flex items-center justify-between">
                        <span>{col.label}</span>
                        {sortField === col.key ? (
                          sortOrder === "asc" ? (
                            <ChevronUpDownIcon className="h-4 w-4 text-gray-900" />
                          ) : (
                            <ChevronDownIcon className="h-4 w-4 text-gray-900" />
                          )
                        ) : (
                          <ChevronUpDownIcon className="h-4 w-4 text-gray-300 opacity-50" />
                        )}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody className="text-sm text-gray-700">
                {pageData.length === 0 ? (
                  <tr>
                    <td colSpan={columns.length} className="text-center py-10 text-gray-500">
                      <div className="flex flex-col items-center gap-2">
                        <MagnifyingGlassIcon className="h-10 w-10 text-gray-300" />
                        <Typography>No records found for this city.</Typography>
                      </div>
                    </td>
                  </tr>
                ) : (
                  pageData.map((row, idx) => (
                    <tr
                      key={idx}
                      className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
                    >
                      {columns.map((col) => (
                        <td
                          key={col.key}
                          className="px-4 py-3 break-words align-top"
                        >
                          {col.key === "name" ? (
                            <span className="font-semibold text-gray-900">
                                {String(row[col.key] ?? "-")}
                            </span>
                          ) : col.key === "website" && row[col.key] ? (
                            <a
                              href={row[col.key]}
                              target="_blank"
                              rel="noreferrer"
                              className="text-blue-600 hover:underline truncate block w-full"
                            >
                              {String(row[col.key])}
                            </a>
                          ) : (
                            String(row[col.key] ?? "-")
                          )}
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

      <div className="mt-6 flex justify-end items-center gap-4">
        <Button
            variant="text"
            className="flex items-center gap-2"
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
        >
            Previous
        </Button>
        <div className="flex items-center gap-2">
            {[...Array(Math.min(5, totalPages))].map((_, i) => {
                 let p = i + 1;
                 if (currentPage > 3 && totalPages > 5) p = currentPage - 2 + i;
                 if (p > totalPages) return null;
                 
                 return (
                    <Button
                        key={p}
                        variant={currentPage === p ? "filled" : "text"}
                        className={`w-8 h-8 p-0 rounded-full ${currentPage === p ? "bg-gray-900" : ""}`}
                        onClick={() => setCurrentPage(p)}
                    >
                        {p}
                    </Button>
                 )
            })}
        </div>
        <Button
            variant="text"
            className="flex items-center gap-2"
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
        >
            Next
        </Button>
      </div>
    </div>
  );
}

export default cities_reports;