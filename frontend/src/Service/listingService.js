import api from '../configs/api';

export const fetchAmazonData = async () => {
  try {

    const response = await api.get('/products/complete'); 

    console.log("Amazon Data Raw:", response.data);
    return response.data.data; 
    
  } catch (error) {
    console.error("Error fetching Amazon data:", error);
    throw error;
  }
};

export const fetchFlipkartData = async () => {
  try {
 
    const response = await api.get('/products/flipkart/complete'); 
    return response.data.data;
  } catch (error) {
    console.error("Flipkart fetch error:", error);
    throw error;
  }
};

// --- ZOMATO (New) ---
export const fetchZomatoData = async () => {
  try {
    const response = await api.get('/products/zomato/complete'); 
    return response.data.data;
  } catch (error) {
    console.error("Zomato fetch error:", error);
    throw error;
  }
};