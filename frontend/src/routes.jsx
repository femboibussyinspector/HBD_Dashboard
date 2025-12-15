import {
  HomeIcon,
  UserCircleIcon,
  TableCellsIcon,
  InformationCircleIcon,
  ServerStackIcon,
  RectangleStackIcon,
  MagnifyingGlassIcon,
  MapPinIcon,
  ShoppingCartIcon,
  CheckCircleIcon,
  XCircleIcon,
  DocumentTextIcon,
  ArrowUpTrayIcon,
} from "@heroicons/react/24/solid";
// import { Home, Profile, Tables, Notifications } from "@/pages/dashboard";
import {Home} from "./pages/dashboard/home";
import { Profile } from "./pages/dashboard/profile";
import { Tables } from "./pages/dashboard/tables";
import { Notifications } from "./pages/dashboard/notifications";
// import { SignUp } from "./pages/auth/sign-up";
// import { SignIn } from "./pages/auth/sign-in";
import BusinessCategory from "./componunts/masterdata/BusinessCategory";
import ServiceCategory from "./componunts/masterdata/ServiceCategory";
import ProductCategory from "./componunts/masterdata/ProductCategory";
import ListingComplate from "./componunts/listing master data/ListingComplate";
import ListingIncomplate from "./componunts/listing master data/ListingIncomplate";
import ProductComplate from "./componunts/product master data/ProductComplate";
import ProductIncomplate from "./componunts/product master data/ProductIncomplate";
import ServiceComplate from "./componunts/service master data/ServiceComplate";
import ServiceIncomplate from "./componunts/service master data/ServiceIncomplate";
import GoogleMapScrapper from "./componunts/scrapper/GoogleMapScrapper";
// import ItemDataImport from "./componunts/data import/ItemDataImport";
import ProductDataImport from "./componunts/data import/ProductDataImport";
import Dasboard2 from "./componunts/Dasboard2";
import ListingDataReport from "./componunts/ListingDataReport";
import ProductDataReport from "./componunts/ProductDataReport";
import MisReportTable from "./componunts/Misreport";
import ListingDataImport from "./componunts/data import/ListingDataImport";
import { element } from "prop-types";
import AmazonScraper from "./componunts/scrapper/AmazonScrapper";
import DuplicateData from "./componunts/listing master data/DuplicateData";
import OthersDataImport from "./componunts/data import/OthersDataImport";
import SearchKeyword from "./componunts/SearchKeyword";
import DmartScrapper from "./componunts/scrapper/DmartScrapper";
import State from "./componunts/masterdata/location msater/State";
import Country from "./componunts/masterdata/location msater/Country";
import Area from "./componunts/masterdata/location msater/Area";
import City from "./componunts/masterdata/location msater/City";
import ListingComplete from "./componunts/listing master data/ListingComplate";
import ProductComplete from "./componunts/product master data/ProductComplate";
import GoogleData from "./componunts/listing master data/GoogleData";
import GoogleMapData from "./componunts/listing master data/GoogleMapData";
import CollegeDuniaData from "./componunts/listing master data/CollegeDuniaData";
import MagicPinData from "./componunts/listing master data/MagicPinData";
import AsklailaData from "./componunts/listing master data/AsklailaData";
import AtmData from "./componunts/listing master data/AtmData";
import JustDialData from "./componunts/listing master data/JustDialData";
import POIndiaData from "./componunts/listing master data/POIndiaData";
import NearBuyData from "./componunts/listing master data/NearBuyData";
import SchoolgisData from "./componunts/listing master data/SchoolgisData";
import YellowPagesData from "./componunts/listing master data/YellowPagesData";
import PindaData from "./componunts/listing master data/PindaData";
import GoogleUploader from "./componunts/data import/GoogleUploader";
import BankDataUploader from "./componunts/data import/BankDataUploader";
import CollegeDuniaUploader from "./componunts/data import/CollegeDuniaUploader";
import HeyPlacesUploader from "./componunts/data import/HeyPlacesUploader";
import AtmUploader from "./componunts/data import/AtmUploader";
import AsklailaUploader from "./componunts/data import/AsklailaUploader";
import PindaUploader from "./componunts/data import/PindaUploader";
import YellowPagesUploader from "./componunts/data import/YellowPagesUploader";
import SchoolgisUploader from "./componunts/data import/SchoolgisUploader";
import NearbuyUploader from "./componunts/data import/NearbuyUploader";
import GoogleMapUploader from "./componunts/data import/GoogleMapUploader";
import JustdialUploader from "./componunts/data import/JustdialUploader";
import FreelistingUploader from "./componunts/data import/FreelistingUploader";
import PostOfficeUploader from "./componunts/data import/PostOfficeUploader";
import ShikshaUploader from "./componunts/data import/ShikshaUploader";
import MagicPinUploader from "./componunts/data import/MagicPinUploader";

const icon = {
  className: "w-5 h-5 text-inherit",
};

export const routes = [
  {
    layout: "dashboard",
    pages: [
      {
        icon: <HomeIcon {...icon} />,
        name: "dashboard",
        path: "/home",
        element: <Home />,
      },
      {
        path:"/listingdata-report",
        element: <MisReportTable ></MisReportTable>, 
        hidden: true, // Hide this from the sidebar
      },
      {
        path:"/productdata-report",
        element: <ProductDataReport />, 
        hidden: true, // Hide this from the sidebar
      },
      {
        icon: <HomeIcon {...icon} />,
        name: "dashboard",
        path: "/home2",
        element: <Dasboard2 />,
      },
      {
        icon: <MagnifyingGlassIcon {...icon} />,
        name: "search Keyword",
        path: "/search-keyword",
        element: <SearchKeyword />,
      },
      {
        icon: <ArrowUpTrayIcon {...icon} />,
        name: "Upload Data",
        children: [
          {
            icon: <ArrowUpTrayIcon {...icon} />,
            name: "Listing Data",
            children: [
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Google",
                path: "/data-imports/listing-data/google-map",
                element: <GoogleUploader />, // Placeholder for Listing Data Report page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "Asklaila",  
                path: "/data-imports/listing-data/asklaila",
                element: <AsklailaUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "Pinda",  
                path: "/data-imports/listing-data/pinda",
                element: <PindaUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "Atm",  
                path: "/data-imports/listing-data/atm",
                element: <AtmUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "Bank",  
                path: "/data-imports/listing-data/bank-data",
                element: <BankDataUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "College Dunia",  
                path: "/data-imports/listing-data/college-dunia",
                element: <CollegeDuniaUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Heyplaces",  
                path: "/data-imports/listing-data/Heyplaces",
                element: <HeyPlacesUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Yellow Pages",  
                path: "/data-imports/listing-data/yellowpages",
                element: <YellowPagesUploader />, // Placeholder for Listing Data Uploader page
              }, {
                icon: <DocumentTextIcon {...icon} />,
                name: "Asklaila",
                path: "/data-imports/listing-data/asklaila",
                element: <AsklailaUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "JustDial",
                path: "/data-imports/listing-data/justdial",
                element: <JustdialUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "PO India",
                patch: "/data-imports/listing-data/po-india",
                element: <PostOfficeUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "Near Buy",
                patch: "/data-imports/listing-data/near-buy",
                element: <NearbuyUploader />, // Placeholder for Listing Data Uploader page
              },{
                icon: <DocumentTextIcon {...icon} />,
                name: "SchoolGis",
                patch: "/data-imports/listing-data/school-gis",
                element: <SchoolgisUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Google Map Scrap Data",  
                path: "/data-imports/listing-data/googlemap-scrap",
                element: <GoogleMapUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Justdial",  
                path: "/data-imports/listing-data/justdial",
                element: <JustdialUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Freelisting",  
                path: "/data-imports/listing-data/freelisting",
                element: <FreelistingUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Post Offices",  
                path: "/data-imports/listing-data/postoffice",
                element: <PostOfficeUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Shiksha",  
                path: "/data-imports/listing-data/shiksha",
                element: <ShikshaUploader />, // Placeholder for Listing Data Uploader page
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Magic Pin",  
                path: "/data-imports/listing-data/magicpin",
                element: <MagicPinUploader />, // Placeholder for Listing Data Uploader page
              },
            ]
          },{
            icon: <DocumentTextIcon {...icon} />,
            name: "Product Data",
            path: "/data-imports/product-data",
            element: <ProductDataImport />, // Placeholder for Product Data page
          },{
            icon: <DocumentTextIcon {...icon} />,
            name: "Others Data",
            path: "/data-imports/others-data",
            element: <OthersDataImport />, // Placeholder for Listing Data page
          }
        ] 
      },
      {
        icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
        name: "Master data",
        children: [
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Location Master",
            children: [
              {
                icon: <TableCellsIcon {...icon} />,
                name: "Country",
                path: "/masterdata/location/country",
                element:<Country />,
              },
              {
                icon: <TableCellsIcon {...icon} />,
                name: "State",
                path: "/masterdata/location/state",
                element:<State />,
              },
              {
                icon: <TableCellsIcon {...icon} />,
                name: "City",
                path: "/masterdata/location/city",
                element:<City />,
              },
              {
                icon: <TableCellsIcon {...icon} />,
                name: "Area",
                path: "/masterdata/location/area",
                element:<Area />,
              },
            ]
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Business Category",
            path: "/masterdata/business-category",
            element:<BusinessCategory />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Service Category",
            path: "/masterdata/service-category",
            element: <ServiceCategory />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Product Category",
            path: "/masterdata/product-category",
            element: <ProductCategory />,
          }
        ]},
      {
        icon: <TableCellsIcon {...icon} />,
        name: "Listing Master Data",
        children: [
          {
            icon:<CheckCircleIcon {...icon} />,
            name: "Complete Data",
            path: "listing-master-data/complete-data",
            element: <ListingComplete/>,
         },{
          icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
          name: "Magicpin",
            path: "listing-master-data/magicpin-data",    
          element:<MagicPinData/>

          },
           {
             icon: <XCircleIcon {...icon} />,
             name: "Google Data",
             path: "listing-master-data/google-data",            
             element:<GoogleData/>
      },
      {
          icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
          name: "Google Maps",
        path: "listing-master-data/googlemap-data", 
          element:<GoogleMapData/>

          },
          {
          icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
          name: "Atm",
            path: "listing-master-data/atm-data",   
          element:<AtmData/>

         },{
          icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
          name: "Bank Data",
          path: "listing-master-data/bank-data",            

         },{
          icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
          name: "College Dunia",
            path: "listing-master-data/collegedunia-data", 
          element:<CollegeDuniaData/>

         },{
          icon: <TableCellsIcon {...icon} />, // <-- Changed to TableCellsIcon for data representation
          name: "Heyplaces",
          path: "listing-master-data/heyplaces-data",            

         },
        //   {
        //     icon: <XCircleIcon {...icon} />,
        //     name: "Incomplete Data",
        //     path: "listing-master-data/incomplete-data",                 -----> Hidden for Testing
        //     element: <ListingIncomplate/>,
        //  },                                                
        //   {
        //     icon: <XCircleIcon {...icon} />,
        //     name: "Duplicate Data",
        //     path: "listing-master-data/duplicate-data",                  -----> Hidden for Testing
        //     element: <DuplicateData/>,
        //   },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "Zomato Data",
          path: "listing-master-data/zomato-data",            
            element:"",
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "Asklaila Data",
          path: "listing-master-data/asklaila-data",            
          element:<AsklailaData/>,
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "JustDial Data",
          path: "listing-master-data/justdial-data",            
          element:<JustDialData/>,
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "PO India Data",
          path: "listing-master-data/poindia-data",            
          element:<POIndiaData/>,
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "Near Buy Data",
          path: "listing-master-data/nearbuy-data",            
          element:<NearBuyData/>,
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "SchoolGis Data",
          path: "listing-master-data/schoolgis-data",            
          element:<SchoolgisData/>,
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "Yellow Pages Data",
          path: "listing-master-data/yellowpages-data",            
          element:<YellowPagesData/>,
          },
        {
          icon: <TableCellsIcon {...icon} />,
          name: "Pinda Data",
          path: "listing-master-data/pinda-data",            
          element:<PindaData/>,
          },

        ]},
      {
        icon: <TableCellsIcon {...icon} />,
        name: "Product Master Data",
        children: [
          {
            icon: <CheckCircleIcon {...icon} />,
            name: "Complete Data",
            path: "product-master-data/complete-data",
            element:<ProductComplete/>,
         },
          {
            icon: <XCircleIcon {...icon} />,
            name: "Incomplete Data",
            path: "product-master-data/incomplete-data",
            element: <ProductIncomplate/>,
         },
        ]
      },
    {
        icon: <TableCellsIcon {...icon} />,
        name: "Service Master Data",
        children: [
          {
            icon: <CheckCircleIcon {...icon} />,
            name: "Complete Data",
            path: "service-master-data/complete-data",
            element: <ServiceComplate/>,
         },
          {
            icon: <XCircleIcon {...icon} />,
            name: "Incomplete Data",
            path: "service-master-data/incomplete-data",
            element: <ServiceIncomplate/>,
         },
        ]
    },
      {
        icon:<MagnifyingGlassIcon {...icon} />,
        name: "Scrapper",
        children: [
          {
            icon:  <MapPinIcon {...icon} />,
            name: "Google Map",
            path: "/scrapper/google-map",
            element: <GoogleMapScrapper />,
          },
          {
            icon:  <ShoppingCartIcon {...icon} />,
            name: "Amazon",
            path:"/scrapper/amazon",
            element:<AmazonScraper/>
          },
          {
            icon:  <ShoppingCartIcon {...icon} />,
            name: "D-mart",
            path:"/scrapper/dmart",
            element:<DmartScrapper/>
          }
        ]
      },
      {
        icon: <UserCircleIcon {...icon} />,
        name: "profile",
        path: "/profile",
        element: <Profile />,
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "tables",
        path: "/tables",
        element: <Tables />,
      },
      {
        icon: <InformationCircleIcon {...icon} />,
        name: "notifications",
        path: "/notifications",
        element: <Notifications />,
      },
    ],
  },

  
];

export default routes;
