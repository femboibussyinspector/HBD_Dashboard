import {
  Card,
  CardBody,
  CardHeader,
  Typography,
  Input,
  Select,
  Option,
  Button,
} from "@material-tailwind/react";
import React, { useMemo, useState } from "react";

/* ---------------- CONFIG ---------------- */

const TABLE_HEADERS = [
  "ASIN",
  "Product_name",
  "price",
  "rating",
  "Number_of_ratings",
  "Brand",
  "Seller",
  "category",
  "subcategory",
  "colour",
  "Author",
  "Manufacturer_Name",
];

const SEARCH_FIELDS = [
  "ASIN",
  "Product_name",
  "Brand",
  "Seller",
  "category",
  "subcategory",
];

/* ---------------- COMPONENT ---------------- */

const ProductCategory = () => {
  const [loading] = useState(false);
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("all");
  const [sortBy, setSortBy] = useState("");
  const [sortOrder, setSortOrder] = useState("asc");
  const [currentPage, setCurrentPage] = useState(1);

  const limit = 8;

  /* 🔹 Replace with API data */
  const data = [];

  /* ---------------- SEARCH + FILTER ---------------- */
  const filteredData = useMemo(() => {
    return data.filter((item) => {
      const matchesSearch = SEARCH_FIELDS.some((field) =>
        String(item[field] ?? "")
          .toLowerCase()
          .includes(search.toLowerCase())
      );

      const matchesCategory =
        categoryFilter === "all" ||
        item.category === categoryFilter;

      return matchesSearch && matchesCategory;
    });
  }, [data, search, categoryFilter]);

  /* ---------------- SORTING ---------------- */
  const sortedData = useMemo(() => {
    if (!sortBy) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aVal = a[sortBy];
      const bVal = b[sortBy];

      if (aVal == null) return 1;
      if (bVal == null) return -1;

      if (typeof aVal === "number") {
        return sortOrder === "asc" ? aVal - bVal : bVal - aVal;
      }

      return sortOrder === "asc"
        ? String(aVal).localeCompare(String(bVal))
        : String(bVal).localeCompare(String(aVal));
    });
  }, [filteredData, sortBy, sortOrder]);

  /* ---------------- PAGINATION ---------------- */
  const totalPages = Math.ceil(sortedData.length / limit);
  const paginatedData = sortedData.slice(
    (currentPage - 1) * limit,
    currentPage * limit
  );

  /* ---------------- FILTER OPTIONS ---------------- */
  const categoryOptions = useMemo(() => {
    return ["all", ...new Set(data.map((d) => d.category).filter(Boolean))];
  }, [data]);

  /* ---------------- CSV EXPORT ---------------- */
  const exportCSV = () => {
    const rows = [TABLE_HEADERS, ...sortedData.map((row) =>
      TABLE_HEADERS.map((h) => `"${row[h] ?? ""}"`)
    )];

    const csv = rows.map((r) => r.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "products.csv";
    a.click();
  };

  return (
    <div className="mt-8 px-4">
      <Card className="border border-gray-200 shadow-sm rounded-xl bg-white">
        {/* ---------- HEADER ---------- */}
        <CardHeader
  floated={false}
  shadow={false}
  className="bg-gray-100 border-b border-gray-300 px-6 py-4 rounded-t-xl"
>
  <div className="flex flex-col md:flex-row gap-4 md:items-center md:justify-between">
    {/* Title */}
    <div>
      <Typography
        variant="h5"
        className="text-gray-800 font-semibold leading-tight"
      >
        Product Category
      </Typography>
    </div>
  </div>
</CardHeader>



        {/* ---------- TABLE ---------- */}
        <CardBody className="px-0 pt-0 pb-2 overflow-x-auto">
          {loading ? (
            <p className="text-center py-10 text-blue-600 font-medium">
              Loading...
            </p>
          ) : (
            <table className="w-full min-w-max table-auto text-left">
              <thead className="sticky top-0 bg-gray-50 z-10">
                <tr>
                  {TABLE_HEADERS.map((head) => (
                    <th
                      key={head}
                      onClick={() => {
                        setSortBy(head);
                        setSortOrder(
                          sortOrder === "asc" ? "desc" : "asc"
                        );
                      }}
                      className="cursor-pointer px-4 py-3 border-b text-xs font-semibold uppercase text-gray-600 hover:bg-gray-100"
                    >
                      <div className="flex items-center gap-1">
                        {head}
                        {sortBy === head && (
                          <span>{sortOrder === "asc" ? "▲" : "▼"}</span>
                        )}
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {paginatedData.length === 0 ? (
                  <tr>
                    <td
                      colSpan={TABLE_HEADERS.length}
                      className="text-center py-10 text-gray-400"
                    >
                      No records found
                    </td>
                  </tr>
                ) : (
                  paginatedData.map((item, idx) => (
                    <tr
                      key={item.ASIN || idx}
                      className="hover:bg-gray-50 transition"
                    >
                      {TABLE_HEADERS.map((key) => (
                        <td
                          key={key}
                          title={item[key]}
                          className="px-4 py-3 text-sm text-gray-700 max-w-[180px] truncate"
                        >
                          {item[key] ?? "-"}
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

      {/* ---------- PAGINATION ---------- */}
      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-6 flex-wrap">
          <Button
            size="sm"
            variant="outlined"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => p - 1)}
          >
            Prev
          </Button>

          {Array.from({ length: totalPages }, (_, i) => (
            <Button
              key={i}
              size="sm"
              onClick={() => setCurrentPage(i + 1)}
              className={
                currentPage === i + 1
                  ? "bg-blue-600"
                  : "bg-white text-gray-700 border"
              }
            >
              {i + 1}
            </Button>
          ))}

          <Button
            size="sm"
            variant="outlined"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => p + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  );
};

export default ProductCategory;
