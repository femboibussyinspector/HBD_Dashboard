import React, { useState } from "react";
import {
  Card,
  CardBody,
  Input,
  Button,
  Typography,
} from "@material-tailwind/react";
import api from "../../utils/Api";

const DmartScraper = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleScrape = async () => {
    if (!searchTerm) {
      setError("Please enter a product name (e.g., 'Maggi' or 'Soap')");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await api.post(
        "/api/scrape_dmart", // Ensure this route exists on your backend
        {
          search_term: searchTerm,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      setResult(response.data);
    } catch (err) {
      console.error("Scraping Error:", err);
      setError(err.response?.data?.error || "Failed to scrape D-Mart data.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-start items-center bg-gray-50 p-4">
      <Card className="w-full max-w-md shadow-lg border border-blue-gray-100">
        <CardBody className="space-y-4">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
               {/* Simple Shopping Bag Icon */}
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="white" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
              </svg>
            </div>
            <Typography variant="h5" color="blue-gray">
              D-Mart Scraper
            </Typography>
          </div>

          <Typography className="text-sm text-gray-600">
            Search for groceries or household items to scrape price and stock data from D-Mart Ready.
          </Typography>

          <Input
            label="Product Name"
            placeholder="e.g. Milk, Rice, Oil"
            shrink={true}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          <Button
            onClick={handleScrape}
            fullWidth
            disabled={loading}
            className="bg-green-600 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <span className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Processing...
              </>
            ) : (
              "Start D-Mart Scrape"
            )}
          </Button>

          {error && (
            <div className="p-3 bg-red-50 rounded-md">
              <Typography color="red" className="text-xs font-medium">
                ⚠️ {error}
              </Typography>
            </div>
          )}

          {result && (
            <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-100">
              <Typography className="text-sm font-bold text-green-800 mb-2">
                Scrape Summary
              </Typography>
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-white p-2 rounded shadow-sm">
                  <Typography className="text-[10px] uppercase text-gray-500 font-bold">Scraped</Typography>
                  <Typography className="text-lg font-black text-blue-gray-900">{result.scraped}</Typography>
                </div>
                <div className="bg-white p-2 rounded shadow-sm">
                  <Typography className="text-[10px] uppercase text-gray-500 font-bold">Database</Typography>
                  <Typography className="text-lg font-black text-blue-gray-900">{result.inserted}</Typography>
                </div>
              </div>
            </div>
          )}
        </CardBody>
      </Card>
    </div>
  );
};

export default DmartScraper;