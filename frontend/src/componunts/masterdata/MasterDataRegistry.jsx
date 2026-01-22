import React, { useState, useEffect } from 'react';
import ReusableTable from '../Table/ReusableTable';

const MasterDataRegistry = () => {
  const [allData, setAllData] = useState([]);
  const [loading, setLoading] = useState(true);

  const columns = [
    { header: "Global ID", accessor: "global_business_id" },
    { header: "Business ID", accessor: "business_id" },
    { header: "Business Name", accessor: "business_name" },
    { header: "Category", accessor: "business_category" },
    { header: "Subcategory", accessor: "business_subcategory" },
    { header: "Ratings", accessor: "ratings" },
    { header: "Reviews", accessor: "reviews" },
    { header: "Primary Phone", accessor: "primary_phone" },
    { header: "Secondary Phone", accessor: "secondary_phone" },
    { header: "Other Phones", accessor: "other_phones" },
    { header: "Virtual Phone", accessor: "virtual_phone" },
    { header: "WhatsApp", accessor: "whatsapp_phone" },
    { header: "Email", accessor: "email" },
    { 
      header: "Website", 
      accessor: "website_url",
      render: (row) => row.website_url ? <a href={row.website_url} target="_blank" rel="noreferrer">Link</a> : "-"
    },
    { 
      header: "Facebook", 
      accessor: "facebook_url",
      render: (row) => row.facebook_url ? <a href={row.facebook_url} target="_blank" rel="noreferrer">FB</a> : "-"
    },
    { 
      header: "LinkedIn", 
      accessor: "linkedin_url",
      render: (row) => row.linkedin_url ? <a href={row.linkedin_url} target="_blank" rel="noreferrer">LI</a> : "-"
    },
    { 
      header: "Twitter", 
      accessor: "twitter_url",
      render: (row) => row.twitter_url ? <a href={row.twitter_url} target="_blank" rel="noreferrer">X</a> : "-"
    },
    { header: "Address", accessor: "address" },
    { header: "Area", accessor: "area" },
    { header: "City", accessor: "city" },
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
    { header: "Description", accessor: "description" },
    { header: "Data Source", accessor: "data_source" },
    { header: "Avg Salary", accessor: "avg_salary" },
    { header: "Admission Req", accessor: "admission_req_list" },
    { header: "Courses", accessor: "courses" }
  ];

  useEffect(() => {
    fetch('http://localhost:5000/api/master_table')
      .then(res => res.json())
      .then(data => {
        setAllData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Full Master Registry (All 36 Fields)</h2>
      {loading ? (
        <p>Fetching massive dataset...</p>
      ) : (
        <ReusableTable columns={columns} data={allData} />
      )}
    </div>
  );
};

export default MasterDataRegistry;