import {
  HomeIcon,
  UserCircleIcon,
  TableCellsIcon,
  InformationCircleIcon,
  ServerStackIcon, // <--- 1. Added Icon for Manager
  RectangleStackIcon,
  MagnifyingGlassIcon,
  MapPinIcon,
  ShoppingCartIcon,
  CheckCircleIcon,
  XCircleIcon,
  DocumentTextIcon,
  ArrowUpTrayIcon,
} from "@heroicons/react/24/solid";

import { Home } from "./pages/dashboard/home";
import { Profile } from "./pages/dashboard/profile";
import { Tables } from "./pages/dashboard/tables";
import { Notifications } from "./pages/dashboard/notifications";
import ZomatoData from "./componunts/listing master data/ZomatoData";
import CitiesReports from "./componunts/Reports/cities_reports";
import CategoriesReports from "./componunts/Reports/categories_reports";
import BusinessCategory from "./componunts/masterdata/BusinessCategory";
import ServiceCategory from "./componunts/masterdata/ServiceCategory";
import HeyPlacesData from "./componunts/listing master data/HeyPlacesData.jsx";
import BankData from "./componunts/listing master data/BankData";
import ProductCategory from "./componunts/masterdata/ProductCategory";
import ListingComplete from "./componunts/listing master data/ListingComplate";
import ListingIncomplate from "./componunts/listing master data/ListingIncomplate";
import ProductComplete from "./componunts/product master data/ProductComplate";
import ProductIncomplate from "./componunts/product master data/ProductIncomplate";

// --- NEW IMPORT ADDED HERE ---
import AmazonData from "./componunts/product master data/AmazonData"; 
import FlipkartData from "./componunts/product master data/FlipkartData";
import BigBasketData from "./componunts/product master data/BigBasket";
import ServiceComplate from "./componunts/service master data/ServiceComplate";
import ServiceIncomplate from "./componunts/service master data/ServiceIncomplate";
import GoogleMapScrapper from "./componunts/scrapper/GoogleMapScrapper";
import ProductDataImport from "./componunts/data import/ProductDataImport";
import CleanListingMaster from "./componunts/clean master data/CleanListingMaster";
import CleanProductMaster from "./componunts/clean master data/CleanProductMaster";
import ListingCategory from "./componunts/masterdata/ListingCategory";
import Dasboard2 from "./componunts/Dasboard2";
import ListingDataReport from "./componunts/ListingDataReport";
import ProductDataReport from "./componunts/ProductDataReport";
import MisReportTable from "./componunts/Misreport";
import ListingDataImport from "./componunts/data import/ListingDataImport";
import AmazonScraper from "./componunts/scrapper/AmazonScrapper";
import DuplicateData from "./componunts/listing master data/DuplicateData";
import OthersDataImport from "./componunts/data import/OthersDataImport";
import SearchKeyword from "./componunts/SearchKeyword";
import DmartScrapper from "./componunts/scrapper/DmartScrapper";
import State from "./componunts/masterdata/location msater/State";
import Country from "./componunts/masterdata/location msater/Country";
import Area from "./componunts/masterdata/location msater/Area";
import City from "./componunts/masterdata/location msater/City";
import GoogleData from "./componunts/listing master data/ShikshaData";
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
import GoogleUploader from "./componunts/data import/ShikshaUploader";
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
import ShikshaData from "./componunts/listing master data/ShikshaData";

// --- 2. Added Scraper Manager Import (Based on your previous file location) ---
import { ScraperManager } from "./layouts/Scrapper_manager";

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
        path: "/listingdata-report",
        element: <MisReportTable />,
        hidden: true,
      },
      {
        path: "/productdata-report",
        element: <ProductDataReport />,
        hidden: true,
      },
      {
        path: "/cities-report",
        element: <CitiesReports />,
        hidden: true,
      },
      {
        path: "/categories-report",
        element: <CategoriesReports />,
        hidden: true,
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
                name: "Asklaila",
                path: "/data-imports/listing-data/asklaila",
                element: <AsklailaUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Pinda",
                path: "/data-imports/listing-data/pinda",
                element: <PindaUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Shiksha",
                path: "/data-imports/listing-data/shiksha",
                element: <ShikshaUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Atm",
                path: "/data-imports/listing-data/atm",
                element: <AtmUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Bank",
                path: "/data-imports/listing-data/bank-data",
                element: <BankDataUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "College Dunia",
                path: "/data-imports/listing-data/college-dunia",
                element: <CollegeDuniaUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Heyplaces",
                path: "/data-imports/listing-data/Heyplaces",
                element: <HeyPlacesUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Yellow Pages",
                path: "/data-imports/listing-data/yellowpages",
                element: <YellowPagesUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "JustDial",
                path: "/data-imports/listing-data/justdial",
                element: <JustdialUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Near Buy",
                path: "/data-imports/listing-data/near-buy",
                element: <NearbuyUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "SchoolGis",
                path: "/data-imports/listing-data/school-gis",
                element: <SchoolgisUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Google Map",
                path: "/data-imports/listing-data/google-map",
                element: <GoogleMapUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Google",
                path: "/data-imports/listing-data/google",
                element: <GoogleUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Freelisting",
                path: "/data-imports/listing-data/freelisting",
                element: <FreelistingUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Post Offices",
                path: "/data-imports/listing-data/postoffice",
                element: <PostOfficeUploader />,
              },
            ],
          },
          {
            icon: <DocumentTextIcon {...icon} />,
            name: "Product Data",
            path: "/data-imports/product-data",
            element: <ProductDataImport />,
          },
          {
            icon: <DocumentTextIcon {...icon} />,
            name: "Others Data",
            path: "/data-imports/others-data",
            element: <OthersDataImport />,
          },
        ],
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "Clean Master Data",
        children: [
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Listing Master",
            path: "/masterdata/clean-listing-master",
            element: <CleanListingMaster />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Product Master",
            path: "/masterdata/clean-product-master",
            element: <CleanProductMaster />,
          },
        ],    
      },
      {
        icon: <TableCellsIcon {...icon} />,
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
                element: <Country />,
              },
              {
                icon: <TableCellsIcon {...icon} />,
                name: "State",
                path: "/masterdata/location/state",
                element: <State />,
              },
              {
                icon: <TableCellsIcon {...icon} />,
                name: "City",
                path: "/masterdata/location/city",
                element: <City />,
              },
              {
                icon: <TableCellsIcon {...icon} />,
                name: "Area",
                path: "/masterdata/location/area",
                element: <Area />,
              },
            ],
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Listing Category",
            path: "/masterdata/listing-category", // Fixed 'paht' typo from original code
            element: <ListingCategory />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Business Category",
            path: "/masterdata/business-category",
            element: <BusinessCategory />,
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
          },
        ],
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "Listing Master Data",
        children: [
          {
            icon: <CheckCircleIcon {...icon} />,
            name: "Complete Data",
            path: "listing-master-data/complete-data",
            element: <ListingComplete />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Magicpin",
            path: "listing-master-data/magicpin-data",
            element: <MagicPinData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Shiksha Data",
            path: "listing-master-data/Shiksha-data",
            element: <ShikshaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Google Maps",
            path: "listing-master-data/google-map-data",
            element: <GoogleMapData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Google Data",
            path: "listing-master-data/google-data",
            element: <GoogleData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Atm",
            path: "listing-master-data/atm-data",
            element: <AtmData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Bank Data",
            path: "listing-master-data/bank-data",
            element: <BankData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "College Dunia",
            path: "listing-master-data/college-dunia-data",
            element: <CollegeDuniaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Heyplaces",
            path: "listing-master-data/heyplaces-data",
            element: <HeyPlacesData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Zomato Data",
            path: "listing-master-data/zomato-data",
            element: "ZomatoData />,",
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Asklaila Data",
            path: "listing-master-data/asklaila-data",
            element: <AsklailaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "JustDial Data",
            path: "listing-master-data/justdial-data",
            element: <JustDialData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "PO India Data",
            path: "listing-master-data/poindia-data",
            element: <POIndiaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Near Buy Data",
            path: "listing-master-data/nearbuy-data",
            element: <NearBuyData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "SchoolGis Data",
            path: "listing-master-data/schoolgis-data",
            element: <SchoolgisData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Yellow Pages Data",
            path: "listing-master-data/yellowpages-data",
            element: <YellowPagesData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Pinda Data",
            path: "listing-master-data/pinda-data",
            element: <PindaData />,
          },
          {
            icon: <XCircleIcon {...icon} />,
            name: "Incomplete Data",
            path: "listing-master-data/incomplete-data",
            element: <ListingIncomplate />,
          }
        ],
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "Product Master Data",
        children: [
          {
            icon: <CheckCircleIcon {...icon} />,
            name: "Complete Data",
            path: "product-master-data/complete-data",
            element: <ProductComplete />,
          },
          {
            icon: <XCircleIcon {...icon} />,
            name: "Incomplete Data",
            path: "product-master-data/incomplete-data",
            element: <ProductIncomplate />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Amazon Data",
            path: "product-master-data/amazon-data",
            element: <AmazonData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Flipkart Data",
            path: "product-master-data/flipkart-data",
            element: <FlipkartData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "BigBasket Data",
            path: "product-master-data/bigbasket-data",
            element: <BigBasketData />,
          }
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
            element: <ServiceComplate />,
          },
          {
            icon: <XCircleIcon {...icon} />,
            name: "Incomplete Data",
            path: "service-master-data/incomplete-data",
            element: <ServiceIncomplate />,
          },
        ],
      },
      
      // --- 3. Scraper Manager Route Added Here ---
      {
        icon: <ServerStackIcon {...icon} />,
        name: "Scraper Manager",
        path: "/scrapper-manager",
        element: <ScraperManager />,
      },
      
      {
        icon: <MagnifyingGlassIcon {...icon} />,
        name: "Scrapper",
        children: [
          {
            icon: <MapPinIcon {...icon} />,
            name: "Google Map",
            path: "/scrapper/google-map",
            element: <GoogleMapScrapper />,
          },
          {
            icon: <ShoppingCartIcon {...icon} />,
            name: "Amazon",
            path: "/scrapper/amazon",
            element: <AmazonScraper />,
          },
          {
            icon: <ShoppingCartIcon {...icon} />,
            name: "D-mart",
            path: "/scrapper/dmart",
            element: <DmartScrapper />,
          },
        ],
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