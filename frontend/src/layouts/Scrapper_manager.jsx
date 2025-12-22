import React, { useState } from "react";
import {
  Card,
  CardHeader,
  CardBody,
  Typography,
  Button,
  Chip,
  Progress,
  Tooltip,
  CardFooter,
} from "@material-tailwind/react";
import {
  PlayIcon,
  StopIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
} from "@heroicons/react/24/solid";

export function ScraperManager() {
  // 1. State for Scrapers Data
  const [scrapers, setScrapers] = useState([
    {
      id: 1,
      name: "Facebook Scraper",
      platform: "Facebook",
      status: "running",
      progress: 65,
      retry: 3,
    },
    {
      id: 2,
      name: "IG Lead Gen",
      platform: "Instagram",
      status: "stopped",
      progress: 0,
      retry: 5,
    },
    {
      id: 3,
      name: "LinkedIn B2B",
      platform: "LinkedIn",
      status: "error",
      progress: 40,
      retry: 2,
    },
  ]);

  // 2. State for Logs
  const [logs, setLogs] = useState([
    {
      time: "14:30:01",
      msg: "Facebook Scraper: Connected to Proxy...",
      type: "info",
    },
    {
      time: "14:30:15",
      msg: "LinkedIn B2B: Error - 403 Forbidden (Auth Expired)",
      type: "error",
    },
    {
      time: "14:31:00",
      msg: "IG Lead Gen: Task Retrying in 5s...",
      type: "warn",
    },
  ]);

  // Handler to delete a row (Frontend logic only)
  const handleDelete = (id) => {
    setScrapers((prev) => prev.filter((scraper) => scraper.id !== id));
  };

  // Helper for status colors
  const getStatusColor = (status) => {
    switch (status) {
      case "running":
        return "green";
      case "error":
        return "red";
      default:
        return "blue-gray";
    }
  };

  return (
    <div className="mt-12 mb-8 flex flex-col gap-12 h-full">
      <Card className="h-full border border-blue-gray-100 shadow-sm">
        {/* --- Header with Grey/White Gradient --- */}
        <CardHeader
          floated={false}
          shadow={false}
          className="m-0 mb-8 p-6 flex justify-between items-center bg-gradient-to-r from-gray-200 via-gray-100 to-white rounded-t-xl border-b border-blue-gray-100"
        >
          <Typography variant="h6" className="text-blue-gray-800">
            Scraper Management
          </Typography>
          <Button
            variant="gradient"
            color="white"
            size="sm"
            className="flex items-center gap-2 border border-blue-gray-100"
          >
            <PlusIcon className="h-4 w-4 text-blue-gray-900" /> 
            <span className="text-blue-gray-900">Add Scraper</span>
          </Button>
        </CardHeader>

        <CardBody className="overflow-x-scroll px-0 pt-0 pb-2">
          <table className="w-full min-w-[640px] table-auto">
            <thead>
              <tr>
                {[
                  "Scraper",
                  "Platform",
                  "Status",
                  "Progress",
                  "Retry Config",
                  "Actions",
                ].map((el) => (
                  <th
                    key={el}
                    className="border-b border-blue-gray-100 py-3 px-5 text-left"
                  >
                    <Typography
                      variant="small"
                      className="text-[11px] font-bold uppercase text-blue-gray-400"
                    >
                      {el}
                    </Typography>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {scrapers.map(
                ({ id, name, platform, status, progress, retry }) => (
                  <tr key={id} className="hover:bg-gray-50 transition-colors">
                    <td className="py-3 px-5 border-b border-blue-gray-50">
                      <Typography
                        variant="small"
                        color="blue-gray"
                        className="font-semibold"
                      >
                        {name}
                      </Typography>
                    </td>
                    <td className="py-3 px-5 border-b border-blue-gray-50">
                      <Typography variant="small" color="blue-gray">
                        {platform}
                      </Typography>
                    </td>
                    <td className="py-3 px-5 border-b border-blue-gray-50">
                      <Chip
                        variant="gradient"
                        color={getStatusColor(status)}
                        value={status}
                        className="py-0.5 px-2 text-[11px] font-medium w-fit uppercase"
                      />
                    </td>
                    <td className="py-3 px-5 border-b border-blue-gray-50 w-64">
                      <div className="w-full">
                        <Typography
                          variant="small"
                          className="mb-1 text-xs font-medium text-blue-gray-600"
                        >
                          {progress}%
                        </Typography>
                        <Progress
                          value={progress}
                          color={status === "error" ? "red" : "blue"}
                          size="sm"
                        />
                      </div>
                    </td>
                    <td className="py-3 px-5 border-b border-blue-gray-50">
                      <Typography
                        variant="small"
                        className="text-xs font-medium text-blue-gray-600"
                      >
                        {retry} retries
                      </Typography>
                    </td>
                    <td className="py-3 px-5 border-b border-blue-gray-50 flex gap-2">
                      <Tooltip
                        content={status === "running" ? "Stop Task" : "Start Task"}
                      >
                        <Button
                          variant="text"
                          size="sm"
                          color={status === "running" ? "red" : "green"}
                        >
                          {status === "running" ? (
                            <StopIcon className="h-4 w-4" />
                          ) : (
                            <PlayIcon className="h-4 w-4" />
                          )}
                        </Button>
                      </Tooltip>

                      <Tooltip content="Edit Config">
                        <Button variant="text" size="sm" color="blue-gray">
                          <PencilIcon className="h-4 w-4" />
                        </Button>
                      </Tooltip>

                      <Tooltip content="Delete Scraper">
                        <Button
                          variant="text"
                          size="sm"
                          color="red"
                          onClick={() => handleDelete(id)}
                        >
                          <TrashIcon className="h-4 w-4" />
                        </Button>
                      </Tooltip>
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </CardBody>
      </Card>

      {/* --- Logs Section (Updated to White-Gray Gradient) --- */}
      <Card className="shadow-sm border border-blue-gray-100">
        <div className="p-4 bg-gradient-to-r from-gray-200 via-gray-100 to-white rounded-xl">
            <Typography
            variant="h6"
            className="mb-2 border-b border-gray-300 pb-2 text-blue-gray-800"
            >
            Live Scraper Logs
            </Typography>
            <div className="h-32 overflow-y-auto no-scrollbar flex flex-col gap-1 font-mono text-sm">
            {logs.map((log, index) => (
                <p
                key={index}
                className={`${
                    log.type === "error"
                    ? "text-red-700 font-semibold"  // Darker red for light background
                    : log.type === "warn"
                    ? "text-orange-700"             // Darker orange for light background
                    : "text-green-700"              // Darker green for light background
                }`}
                >
                <span className="text-gray-600 font-bold">[{log.time}]</span> {log.msg}
                </p>
            ))}
            </div>
        </div>
      </Card>

      {/* --- Footer Section --- */}
      <Card className="mt-auto p-4 text-center border border-blue-gray-50 rounded-xl shadow-sm bg-gradient-to-r from-gray-50 to-white">
        <Typography variant="small" className="font-normal text-blue-gray-600">
          © {new Date().getFullYear()} HBD Dashboard. All rights reserved.
          Outsourced Scraper Module v1.0
        </Typography>
      </Card>
    </div>
  );
}

export default ScraperManager;