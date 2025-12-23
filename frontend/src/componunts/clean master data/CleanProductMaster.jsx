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
import { ChevronUpDownIcon } from "@heroicons/react/24/solid";
import * as XLSX from "xlsx/dist/xlsx.full.min.js";
import { amazonProductData } from "@/data/amazonJSON";

/* -------------------- Constants -------------------- */

const LIMIT = 20;

const COLUMNS = [
  { key: "source", label: "Source", width: 120 },
  { key: "ASIN", label: "ASIN", width: 140 },
  { key: "title", label: "Product Title", width: 350 },
  { key: "price", label: "Price", width: 100 },
  { key: "rating", label: "Rating", width: 90 },
  { key: "review_count", label: "Reviews", width: 110 },
  { key: "best_seller_rank", label: "BSR", width: 150 },
  { key: "brand", label: "Brand", width: 130 },
  { key: "availability", label: "Stock Status", width: 120 },
  { key: "category", label: "Main Category", width: 180 },
  { key: "url", label: "Product Link", width: 250 },
  { key: "image_url", label: "Image Link", width: 200 },
  { key: "manufacturer", label: "Manufacturer", width: 180 },
];

/* -------------------- Utils -------------------- */

const safeLower = (v) => String(v ?? "").toLowerCase();

const convertToCSV = (rows) => {
  if (!rows.length) return "";
  const headers = Object.keys(rows[0]);
  const body = rows.map((r) =>
    headers.map((h) => `"${String(r[h] ?? "").replace(/"/g, "'")}"`).join(",")
  );
  return [headers.join(","), ...body].join("\n");
};

/* -------------------- Component -------------------- */

const CleanProductMaster = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);

  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [categorySearch, setCategorySearch] = useState("");
  const [source, setSource] = useState("");

  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  /* -------------------- Load Data -------------------- */

  useEffect(() => {
    setTimeout(() => {
      setData(amazonProductData);
      setLoading(false);
    }, 300);
  }, []);

  /* -------------------- Filtering -------------------- */

  const filteredData = useMemo(() => {
    return data.filter((x) => {
      if (search && !safeLower(x.title).includes(search.toLowerCase()))
        return false;

      if (
        categorySearch &&
        !safeLower(x.category).includes(categorySearch.toLowerCase())
      )
        return false;

      if (source && safeLower(x.source) !== source) return false;

      return true;
    });
  }, [data, search, categorySearch, source]);

  /* -------------------- Sorting -------------------- */

  const sortedData = useMemo(() => {
    if (!sortField) return filteredData;

    return [...filteredData].sort((a, b) => {
      const A = safeLower(a[sortField]);
      const B = safeLower(b[sortField]);
      if (A === B) return 0;
      return sortOrder === "asc" ? (A > B ? 1 : -1) : A < B ? 1 : -1;
    });
  }, [filteredData, sortField, sortOrder]);

  /* -------------------- Pagination -------------------- */

  const totalPages = Math.max(1, Math.ceil(sortedData.length / LIMIT));

  const pageData = useMemo(() => {
    const start = (page - 1) * LIMIT;
    return sortedData.slice(start, start + LIMIT);
  }, [sortedData, page]);

  useEffect(() => {
    setPage(1);
  }, [search, categorySearch, source]);

  /* -------------------- Actions -------------------- */

  const toggleSort = (field) => {
    if (field === sortField) {
      setSortOrder((o) => (o === "asc" ? "desc" : "asc"));
    } else {
      setSortField(field);
      setSortOrder("asc");
    }
  };

  const downloadCSV = (currentOnly) => {
    const rows = currentOnly ? pageData : sortedData;
    const blob = new Blob([convertToCSV(rows)], {
      type: "text/csv;charset=utf-8;",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = currentOnly ? "product_page.csv" : "product_all.csv";
    a.click();
  };

  const downloadExcel = (currentOnly) => {
    const rows = currentOnly ? pageData : sortedData;
    if (!rows.length) return;

    const ws = XLSX.utils.json_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Products");
    XLSX.writeFile(
      wb,
      currentOnly ? "product_page.xlsx" : "product_all.xlsx"
    );
  };

  /* -------------------- UI -------------------- */

  return (
    <div className="min-h-screen mt-8 mb-12 px-4 bg-white text-black">
      <div className="flex justify-between mb-4">
        <Typography variant="h4" className="pb-2">
          Clean Product Data
        </Typography>
        <div className="flex gap-2">
          <Button size="sm" onClick={() => downloadCSV(false)}>CSV All</Button>
          <Button size="sm" onClick={() => downloadCSV(true)}>CSV Page</Button>
          <Button size="sm" onClick={() => downloadExcel(false)}>Excel All</Button>
          <Button size="sm" onClick={() => downloadExcel(true)}>Excel Page</Button>
        </div>
      </div>

      <Card>
        <CardHeader className="flex flex-wrap gap-3 p-4 bg-gray-100">
          <Input
            label="Search Name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <Input
            label="Search Category"
            value={categorySearch}
            onChange={(e) => setCategorySearch(e.target.value)}
          />
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="border rounded px-3 py-2 bg-gray-100"
          >
            <option value="">All Sources</option>
            <option value="amazon">Amazon</option>
            <option value="flipkart">Flipkart</option>
            <option value="bigbasket">BigBasket</option>
            <option value="jio-mart">Jio Mart</option>
            <option value="d-mart">D-Mart</option>
          </select>

          <div className="ml-auto flex gap-2">
            <Button size="sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</Button>
            <Button size="sm" disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>Next</Button>
          </div>
        </CardHeader>

        <CardBody className="p-0 overflow-x-auto">
          {loading ? (
            <div className="flex justify-center py-10">
              <Spinner />
            </div>
          ) : (
            <table className="w-full min-w-[1500px] table-fixed">
              <thead className="bg-gray-200 sticky top-0">
                <tr>
                  {COLUMNS.map((c) => (
                    <th
                      key={c.key}
                      style={{ width: c.width }}
                      className="px-3 py-2"
                    >
                      <div
                        className="flex gap-2 cursor-pointer"
                        onClick={() => toggleSort(c.key)}
                      >
                        {c.label}
                        <ChevronUpDownIcon className="h-4" />
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {pageData.length === 0 ? (
                  <tr>
                    <td
                      colSpan={COLUMNS.length}
                      className="text-center p-10 text-gray-500"
                    >
                      No product data found.
                    </td>
                  </tr>
                ) : (
                  pageData.map((row, index) => (
                    <tr
                      key={index}
                      className="even:bg-blue-gray-50/50 hover:bg-blue-50/50 transition-colors"
                    >
                      {COLUMNS.map((col) => (
                        <td
                          key={col.key}
                          className="p-4 text-sm border-b border-blue-gray-50 truncate"
                        >
                          {col.key === "url" || col.key === "image_url"? (
                            <a
                              href={row[col.key]}
                              target="_blank"
                              rel="noreferrer"
                              className="text-blue-600 font-medium hover:underline"
                            >
                              View Link
                            </a>
                          ) : col.key === "price" ? (
                            <span className="font-bold text-green-700">
                              ₹{row[col.key] || "0.00"}
                            </span>
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

export default CleanProductMaster;
