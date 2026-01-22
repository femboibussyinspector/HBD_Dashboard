import React, { useState } from "react";
import {
  Card,
  CardBody,
  Input,
  Select,
  Option,
  Button,
  Typography,
} from "@material-tailwind/react";

export default function SearchKeyword() {
  const [searchType, setSearchType] = useState("business");
  const [formData, setFormData] = useState({
    location: "",
    category: "",
    keyword: "",
  });
  const [results, setResults] = useState([]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSearch = async () => {
    // 1. Updated Mock Data to include 'category'
    const mockData = [
      { id: 1, name: "CityMart", type: "Business", category: "Shopping", location: "Ahmedabad" },
      { id: 2, name: "Sweet Shop", type: "Product", category: "Food", location: "Surat" },
      { id: 3, name: "Plumbing Services", type: "Service", category: "Others", location: "Vadodara" },
      { id: 4, name: "Apollo Pharmacy", type: "Business", category: "Health", location: "Ahmedabad" },
    ];

    // filter mock data
    const filtered = mockData.filter(
      (item) =>
        item.type.toLowerCase() === searchType &&
        (item.location.toLowerCase().includes(formData.location.toLowerCase()) ||
          item.name.toLowerCase().includes(formData.keyword.toLowerCase()))
    );
    setResults(filtered);
  };

  return (
    <div className="flex flex-col items-center p-5 min-h-screen bg-gray-50 mt-8">

      <Card className="w-full max-w-3xl shadow-lg">
        <CardBody>
          <Typography variant="h4" className="mb-6 text-center font-semibold">
            Search {searchType.charAt(0).toUpperCase() + searchType.slice(1)} Data
          </Typography>

          {/* Search Type Selection */}
          <div className="flex flex-wrap justify-center mb-6 gap-4">
            {["business", "product", "service"].map((type) => (
              <Button
                key={type}
                className="w-full sm:w-auto"
                onClick={() => setSearchType(type)}
                color={searchType === type ? "blue" : "gray"}
                variant={searchType === type ? "filled" : "outlined"}
              >
                {type.charAt(0).toUpperCase() + type.slice(1)}
              </Button>
            ))}
          </div>

          {/* Dynamic Form Fields */}
          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <Input
              label="Enter Location"
              name="location"
              value={formData.location}
              onChange={handleChange}
            />

            {(searchType === "business" ||
              searchType === "product" ||
              searchType === "service") && (
              <Select
                label={`Select ${searchType.charAt(0).toUpperCase() + searchType.slice(1)} Category`}
                name="category"
                value={formData.category}
                onChange={(val) => setFormData({ ...formData, category: val })}
              >
                <Option value="food">Food</Option>
                <Option value="shopping">Shopping</Option>
                <Option value="health">Health</Option>
                <Option value="others">Others</Option>
              </Select>
            )}
          </div>

          {/* Keyword Search */}
          <div className="mb-4">
            <Input
              label="Custom Keyword"
              name="keyword"
              value={formData.keyword}
              onChange={handleChange}
            />
          </div>

          <div className="flex justify-center">
            <Button color="blue" onClick={handleSearch}>
              Search
            </Button>
          </div>
        </CardBody>
      </Card>

      {/* Results Table */}
      {results.length > 0 && (
        <Card className="w-full max-w-3xl mt-6 shadow-md">
          <CardBody>
            <Typography variant="h5" className="mb-4 font-semibold text-center">
              Search Results
            </Typography>
            <div className="overflow-x-auto">
              <table className="w-full text-left border border-gray-200 rounded-lg">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="p-3 border-b">#</th>
                    <th className="p-3 border-b">Name</th>
                    <th className="p-3 border-b">Type</th>
                    {/* Added Category Header */}
                    <th className="p-3 border-b">Category</th>
                    <th className="p-3 border-b">Location</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((item, idx) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="p-3 border-b">{idx + 1}</td>
                      <td className="p-3 border-b">{item.name}</td>
                      <td className="p-3 border-b">{item.type}</td>
                      {/* Added Category Data */}
                      <td className="p-3 border-b">{item.category}</td>
                      <td className="p-3 border-b">{item.location}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
}