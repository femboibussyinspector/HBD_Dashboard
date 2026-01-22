import React, { useState } from 'react';
// IMPORT PATH: Check this carefully. 
// Screenshot ke hisab se ye file aur Table folder same jagah hain.
import ReusableTable from './Table/ReusableTable'; 

const ListingDataReport = () => {
  // 1. CONFIGURATION (Jo list tune di thi)
  const columns = [
    { header: 'Global Biz ID', accessor: 'global_business_id' },
    { header: 'Business ID', accessor: 'business_id' },
    { header: 'Business Name', accessor: 'business_name' }, // Ensure backend sends 'business_name' not 'business name'
    { header: 'Category', accessor: 'business_category' },
    { header: 'Subcategory', accessor: 'business_subcategory' },
    { header: 'Ratings', accessor: 'ratings' },
    { header: 'Primary Phone', accessor: 'primary_phone' },
    { header: 'Secondary Phone', accessor: 'secondary_phone' },
    { header: 'Other Phones', accessor: 'other_phones' },
    { header: 'Virtual Phone', accessor: 'virtual_phone' },
    { header: 'Whatsapp', accessor: 'whatsapp_phone' },
    { header: 'Email', accessor: 'email' },
    { 
      header: 'Website', 
      accessor: 'website_url',
      render: (row) => row.website_url ? <a href={row.website_url} target="_blank" rel="noreferrer">Link</a> : '-'
    },
    { 
      header: 'Facebook', 
      accessor: 'facebook_url',
      render: (row) => row.facebook_url ? <a href={row.facebook_url} target="_blank" rel="noreferrer">FB</a> : '-'
    },
    { 
      header: 'LinkedIn', 
      accessor: 'linkedin_url',
      render: (row) => row.linkedin_url ? <a href={row.linkedin_url} target="_blank" rel="noreferrer">IN</a> : '-'
    },
    { 
      header: 'Twitter', 
      accessor: 'twitter_url',
      render: (row) => row.twitter_url ? <a href={row.twitter_url} target="_blank" rel="noreferrer">TW</a> : '-'
    },
    { header: 'Address', accessor: 'address' },
    { header: 'Area', accessor: 'area' },
    { header: 'City', accessor: 'city' },
    { header: 'State', accessor: 'state' },
    { header: 'Pincode', accessor: 'pincode' },
    { header: 'Country', accessor: 'country' },
    { header: 'Latitude', accessor: 'latitude' },
    { header: 'Longitude', accessor: 'longitude' },
    { header: 'Avg Fees', accessor: 'avg_fees' },
    { header: 'Course Details', accessor: 'course_details' },
    { header: 'Duration', accessor: 'duration' },
    { header: 'Requirement', accessor: 'requirement' },
    { header: 'Avg Spent', accessor: 'avg_spent' },
    { header: 'Cost for Two', accessor: 'cost_for_two' },
    { header: 'Reviews', accessor: 'reviews' },
    { header: 'Description', accessor: 'description' },
    { header: 'Data Source', accessor: 'data_source' },
    { header: 'Avg Salary', accessor: 'avg_salary' },
    { header: 'Admission Req', accessor: 'admission_req_list' },
    { header: 'Courses', accessor: 'courses' }
  ];

  // 2. DUMMY DATA (Jab tak backend se data nahi aata, testing ke liye)
  const dummyData = [
    {
      global_business_id: "GB001",
      business_id: "BZ101",
      business_name: "Tech Solutions",
      business_category: "IT",
      city: "Bhopal",
      ratings: "4.5",
      primary_phone: "9876543210",
      email: "info@tech.com",
      website_url: "https://google.com"
    }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>Listing Data Report</h2>
      {/* Table Call */}
      <ReusableTable columns={columns} data={dummyData} />
    </div>
  );
};

export default ListingDataReport;