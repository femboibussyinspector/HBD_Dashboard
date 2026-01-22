import React, { useState, useEffect } from 'react';
import ReusableTable from '../Table/ReusableTable'; 

const AmazonData = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // 1. CONFIGURATION: Define how to show the data
  const amazonColumns = [
    {
      header: "Image",
      accessor: "img",
      render: (row) => (
        <img 
          src={row.img} 
          alt="product" 
          style={{ width: "50px", height: "50px", objectFit: "contain" }} 
        />
      )
    },
    {
      header: "Product Name",
      accessor: "name",
      render: (row) => (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontWeight: 'bold' }}>{row.name}</span>
          <span style={{ fontSize: '12px', color: '#666' }}>ID: {row.id}</span>
        </div>
      )
    },
    {
      header: "Price",
      accessor: "price",
      render: (row) => (
        <span style={{ fontWeight: 'bold' }}>₹{row.price}</span>
      )
    },
    {
      header: "Rating",
      accessor: "rating",
      render: (row) => <span>{row.rating} ⭐</span>
    },
    {
      header: "Action",
      accessor: "action",
      render: (row) => (
        <button 
           style={{ padding: '5px 10px', cursor: 'pointer' }}
           onClick={() => alert(`View details for ${row.name}`)}
        >
          View
        </button>
      )
    }
  ];

  // 2. FETCHING: Get data from Flask
  useEffect(() => {
    // Replace this URL with your actual Flask API endpoint
    fetch('http://localhost:5000/api/amazon-products')
      .then((response) => response.json())
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h2>Amazon Product Master</h2>
      {loading ? (
        <p>Loading data...</p>
      ) : (
        <ReusableTable columns={amazonColumns} data={products} />
      )}
    </div>
  );
};

export default AmazonData;