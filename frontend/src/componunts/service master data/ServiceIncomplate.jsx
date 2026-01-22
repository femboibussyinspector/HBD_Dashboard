import React, { useEffect, useMemo, useState } from "react";
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Spinner,
} from "@material-tailwind/react";
import {
  MagnifyingGlassIcon,
  ChevronUpDownIcon,
  ChevronDownIcon,
} from "@heroicons/react/24/solid";
// TODO: Ensure you have this data file or replace with mock data
import { productData } from "@/data/productJSON"; 
import * as XLSX from "xlsx/dist/xlsx.full.min.js";

const defaultColumns = [
  { key: "ASIN", label: "ASIN", width: 150 },
  { key: "Product_name", label: "Service Name", width: 300 },
  { key: "price", label: "Price", width: 100 },
  { key: "rating", label: "Rating", width: 100 },
  { key: "category", label: "Category", width: 180 },
  { key: "link", label: "Link", width: 250 },
  // ... add other columns as needed
];

const ServiceIncomplete = () => {
  // --- STATE MANAGEMENT ---
  const [loading, setLoading] = useState(false); // Initially false for now
  const [fullData, setFullData] = useState([]);
  const [pageData, setPageData] = useState([]); // The data currently displayed on screen
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0);
  const limit = 10;

  const [search, setSearch] = useState("");
  const [areaSearch, setAreaSearch] = useState("");

  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  const [columns, setColumns] = useState(defaultColumns);

  // --- 1. DATA FETCHING ---
  useEffect(() => {
    // TODO: Simulate an API call. 
    // 1. Set loading to true.
    // 2. Use setTimeout to wait 300ms.
    // 3. Set 'fullData' to 'productData'.
    // 4. Set 'total' to the length of the data.
    // 5. Set loading to false.
    
    console.log("Fetching data...");
  }, []);

  // --- 2. FILTERING LOGIC ---
  const filteredData = useMemo(() => {
    let data = [...fullData];

    // TODO: Implement Search Logic
    // If 'search' state has a value, filter 'data' by 'Product_name'.
    
    // TODO: Implement Category Search Logic
    // If 'areaSearch' state has a value, filter 'data' by 'category'.

    return data;
  }, [fullData, search, areaSearch]);

  // --- 3. SORTING LOGIC ---
  const sortedData = useMemo(() => {
    if (!sortField) return filteredData;

    // TODO: Implement Sorting Logic
    // Sort 'filteredData' based on 'sortField' and 'sortOrder' (asc/desc).
    // Remember to handle string vs number comparisons if necessary.

    return filteredData; // Placeholder return
  }, [filteredData, sortField, sortOrder]);

  // --- 4. PAGINATION LOGIC ---
  useEffect(() => {
    // TODO: Calculate the slice of data to show based on 'currentPage' and 'limit'.
    // 1. Calculate 'start' index.
    // 2. Slice 'sortedData'.
    // 3. Update 'pageData' state.
    // 4. Update 'total' state (in case filtering changed the count).

  }, [sortedData, currentPage]);

  const totalPages = Math.ceil(total / limit) || 1;

  const toggleSort = (field) => {
    // TODO: specific logic to toggle between 'asc', 'desc' or reset.
    // Update 'sortField' and 'sortOrder'.
    console.log("Sort requested for:", field);
  };

  // --- 5. EXPORT LOGIC ---
  const convertToCSV = (arr) => {
     // TODO: Helper function to convert JSON array to CSV string.
     return "";
  };

  const downloadCSV = (currentOnly = false) => {
    // TODO: Implement CSV download.
    // 1. Determine which data to use (pageData vs fullData).
    // 2. Convert to CSV.
    // 3. Create a Blob and trigger a download via an anchor tag.
    alert("CSV Download not implemented yet");
  };

  const downloadExcel = (currentOnly = false) => {
    // TODO: Implement Excel download using XLSX library.
    alert("Excel Download not implemented yet");
  };

  // --- 6. RESIZE LOGIC ---
  const startResize = (colKey, e) => {
    // TODO: Implement column resizing using mouse events.
    // 1. Capture starting X position.
    // 2. Add event listeners for 'mousemove' and 'mouseup'.
    // 3. Update column width in state.
    e.preventDefault();
    console.log("Resize started for:", colKey);
  };

  return (
    <div className="min-h-screen mt-8 mb-12 px-4">
      <div className="flex justify-between items-center mb-4">
        <Typography variant="h4">Service Data (Incomplete)</Typography>

        <div className="flex items-center gap-2">
          <Button size="sm" onClick={() => downloadCSV(false)}>CSV All</Button>
          <Button size="sm" onClick={() => downloadCSV(true)}>CSV Page</Button>
          <Button size="sm" onClick={() => downloadExcel(false)}>Excel All</Button>
          <Button size="sm" onClick={() => downloadExcel(true)}>Excel Page</Button>
        </div>
      </div>

      <Card>
        <CardHeader className="flex flex-wrap items-center justify-between gap-3 p-4 bg-gray-100">
          <div className="flex gap-3 items-center flex-wrap">
            <Input
              label="Search Name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <Input
              label="Search Category..."
              value={areaSearch}
              onChange={(e) => setAreaSearch(e.target.value)}
              icon={<MagnifyingGlassIcon className="h-5 w-5" />}
            />
          </div>

          <div className="flex gap-2 items-center">
             {/* Pagination Controls */}
            <div>
              Page {currentPage} / {totalPages}
            </div>
            <Button
              size="sm"
              onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            >
              Prev
            </Button>
            <Button
              size="sm"
              onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </Button>
          </div>
        </CardHeader>

        <CardBody className="p-0 overflow-x-auto">
          {loading ? (
            <div className="flex justify-center py-10">
              <Spinner className="h-10 w-10" />
            </div>
          ) : (
            <table className="w-full table-fixed border-collapse min-w-[1500px]">
              <thead className="sticky top-0 z-20 border-b bg-gray-100">
                <tr>
                  {columns.map((col) => (
                    <th
                      key={col.key}
                      style={{ width: col.width }}
                      className="px-3 py-2 text-left relative select-none"
                    >
                      <div className="flex items-center justify-between">
                        <div
                          className="flex items-center gap-2 cursor-pointer"
                          onClick={() => toggleSort(col.key)}
                        >
                          <span className="capitalize text-sm font-semibold">
                            {col.label}
                          </span>
                          {/* Visual indicator logic for sorting */}
                          {sortField === col.key ? (
                             sortOrder === "asc" ? <ChevronUpDownIcon className="h-4" /> : <ChevronDownIcon className="h-4" />
                          ) : (
                            <ChevronUpDownIcon className="h-4 opacity-40" />
                          )}
                        </div>
                        
                        {/* Resizer Handle */}
                        <div
                          onMouseDown={(e) => startResize(col.key, e)}
                          className="absolute right-0 top-0 h-full w-2 cursor-col-resize hover:bg-gray-300"
                        ></div>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {pageData.length === 0 ? (
                  <tr>
                    <td colSpan={columns.length} className="text-center p-6 text-gray-500">
                      {fullData.length === 0 ? "No data loaded yet (Check useEffect)" : "No records found matching filters"}
                    </td>
                  </tr>
                ) : (
                  pageData.map((row, i) => (
                    <tr key={i} className="border-b hover:bg-gray-50">
                      {columns.map((col) => (
                        <td
                          key={col.key}
                          style={{ width: col.width }}
                          className="px-3 py-3 break-words text-sm"
                        >
                          {col.key === "link" && row[col.key] ? (
                            <a href={row[col.key]} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
                              Link
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
    </div>
  );
};

export default ServiceIncomplete;