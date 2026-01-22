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

import MasterDataRegistry from "./componunts/masterdata/MasterDataRegistry";
import { Home } from "./pages/dashboard/home";
import { Profile } from "./pages/dashboard/profile";
import { Tables } from "./pages/dashboard/tables";
import { Notifications } from "./pages/dashboard/notifications";
import ZomatoData from "./componunts/product master data/ZomatoData";
import CitiesReports from "./componunts/Reports/cities_reports";
import CategoriesReports from "./componunts/Reports/categories_reports";
// --- NEW REPORT IMPORTS ---
import CitiesPendingReport from "./componunts/Reports/CitiesPendingReport";
import CategoriesPendingReport from "./componunts/Reports/CategoriesPendingReport";
// --------------------------
import BusinessCategory from "./componunts/masterdata/BusinessCategory";
import ServiceCategory from "./componunts/masterdata/ServiceCategory";
import HeyPlacesData from "./componunts/listing master data/HeyPlacesData.jsx";
import BankData from "./componunts/listing master data/BankData";
import ProductCategory from "./componunts/masterdata/ProductCategory";
import ListingComplete from "./componunts/listing master data/ListingComplate";
import ListingIncomplate from "./componunts/listing master data/ListingIncomplate";
import ProductComplete from "./componunts/product master data/ProductComplate";
import ProductIncomplate from "./componunts/product master data/ProductIncomplate";
import AmazonData from "./componunts/product master data/AmazonData"; 
import FlipkartData from "./componunts/product master data/FlipkartData";
import BigBasketData from "./componunts/product master data/BigBasket";
import ServiceComplate from "./componunts/service master data/ServiceComplate";
import ServiceIncomplate from "./componunts/service master data/ServiceIncomplate";
import GoogleMapScrapper from "./componunts/scrapper/GoogleMapScrapper";
import CleanListingMaster from "./componunts/clean master data/CleanListingMaster";
import CleanProductMaster from "./componunts/clean master data/CleanProductMaster";
import ListingCategory from "./componunts/masterdata/ListingCategory";
import ReportDashboard from "./componunts/ReportDashboard";
import ListingDataReport from "./componunts/ListingDataReport";
import ProductDataReport from "./componunts/ProductDataReport";
import MisReportTable from "./componunts/Misreport";
import AmazonScraper from "./componunts/scrapper/AmazonScrapper";
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
import GoogleUploader from "./componunts/data import/listing import/GoogleUploader";
import BankDataUploader from "./componunts/data import/listing import/BankDataUploader";
import CollegeDuniaUploader from "./componunts/data import/listing import/CollegeDuniaUploader";
import HeyPlacesUploader from "./componunts/data import/listing import/HeyPlacesUploader";
import AtmUploader from "./componunts/data import/listing import/AtmUploader";
import AsklailaUploader from "./componunts/data import/listing import/AsklailaUploader";
import PindaUploader from "./componunts/data import/listing import/PindaUploader";
import YellowPagesUploader from "./componunts/data import/listing import/YellowPagesUploader";
import SchoolgisUploader from "./componunts/data import/listing import/SchoolgisUploader";
import NearbuyUploader from "./componunts/data import/listing import/NearbuyUploader";
import GoogleMapUploader from "./componunts/data import/listing import/GoogleMapUploader";
import JustdialUploader from "./componunts/data import/listing import/JustdialUploader";
import FreelistingUploader from "./componunts/data import/listing import/FreelistingUploader";
import PostOfficeUploader from "./componunts/data import/listing import/PostOfficeUploader";
import ShikshaUploader from "./componunts/data import/listing import/ShikshaUploader";
import DuplicateData from "./componunts/listing master data/DuplicateData";
import ShikshaData from "./componunts/listing master data/ShikshaData";
import FlipkartScrapper from "./componunts/scrapper/FlipkartScrapper";
import IndiamartScrapper from "./componunts/scrapper/IndiamartScrapper";
import BlinkitScrapper from "./componunts/scrapper/BlinkitScrapper";
import ZeptoScrapper from "./componunts/scrapper/ZeptoScrapper";
import JiomartScrapper from "./componunts/scrapper/JiomartScrapper";
import ZomatoScrapper from "./componunts/scrapper/ZomatoScrapper";
import BigbasketScrapper from "./componunts/scrapper/BigbasketScrapper";
import JioMartData from "./componunts/product master data/JioMart";
import DmartData from "./componunts/product master data/DMart";
import ZeptoData from "./componunts/product master data/Zepto";
import BlinkIt from "./componunts/product master data/BlinkIt";
import IndiaMart from "./componunts/product master data/IndiaMart";
import AmazonUploader from "./componunts/data import/product import/AmazonUploader";
import BigBasketUploader from "./componunts/data import/product import/BigBasketUploader";
import BlinkitUploader from "./componunts/data import/product import/BlinkitUploader";
import DMartUploader from "./componunts/data import/product import/DMartuploader";
import FlipkartUploader from "./componunts/data import/product import/FlipkartUploader";
import IndiaMartUploader from "./componunts/data import/product import/IndiaMartUploader";
import JioMartUploader from "./componunts/data import/product import/JioMartUploader";
import ZeptoUploader from "./componunts/data import/product import/ZeptoUploader";
import { ScraperManager } from "./layouts/Scrapper_manager";
import ZomatoUploader from "./componunts/data import/product import/ZomatoUploader";
import { element } from "prop-types";

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
      // --- NEW ROUTES ADDED HERE ---
      {
        path: "/cities-pending-report",
        element: <CitiesPendingReport />,
        hidden: true,
      },
      {
        path: "/categories-pending-report",
        element: <CategoriesPendingReport />,
        hidden: true,
      },
      // -----------------------------
      {
        icon: <HomeIcon {...icon} />,
        name: "Data Report",
        path: "/home2",
        element: <ReportDashboard />,
      },
      // ... (Rest of your code remains unchanged)
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
                name: "ATM",
                path: "/data-imports/listing-data/atm",
                element: <AtmUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Bank Data",
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
                name: "Freelisting",
                path: "/data-imports/listing-data/freelisting",
                element: <FreelistingUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Google Maps",
                path: "/data-imports/listing-data/google-maps",
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
                name: "Hey Places",
                path: "/data-imports/listing-data/hey-places",
                element: <HeyPlacesUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Just Dial",
                path: "/data-imports/listing-data/just-dial",
                element: <JustdialUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "NearBuy",
                path: "/data-imports/listing-data/nearbuy",
                element: <NearbuyUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Pinda",
                path: "/data-imports/listing-data/pinda",
                element: <PindaUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Post Office",
                path: "/data-imports/listing-data/post-office",
                element: <PostOfficeUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Schoolgis",
                path: "/data-imports/listing-data/schoolgis",
                element: <SchoolgisUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Shiksha",
                path: "/data-imports/listing-data/shiksha",
                element: <ShikshaUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Yellow Pages",
                path: "/data-imports/listing-data/yellow-pages",
                element: <YellowPagesUploader />,
              }
            ],
          },
          {
            icon: <ArrowUpTrayIcon {...icon} />,
            name: "Product Data",
            children: [
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Amazon",
                path: "/data-imports/product-data/amazon",
                element: <AmazonUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "BigBasket",
                path: "/data-imports/product-data/big-basket",
                element: <BigBasketUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Blinkit",
                path: "/data-imports/product-data/blinkit",
                element: <BlinkitUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "D-Mart",
                path: "/data-imports/product-data/d-mart",
                element: <DMartUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Flipkart",
                path: "/data-imports/product-data/flipkart",
                element: <FlipkartUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "India Mart",
                path: "/data-imports/product-data/india-mart",
                element: <IndiaMartUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "JioMart",
                path: "/data-imports/product-data/jio-mart",
                element: <JioMartUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Zepto",
                path: "/data-imports/product-data/zepto",
                element: <ZeptoUploader />,
              },
              {
                icon: <DocumentTextIcon {...icon} />,
                name: "Zomato",
                path: "/data-imports/product-data/zomato",
                element: <ZomatoUploader />,
              }
            ],
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
            name: "Master Data Registry",
            path: "/masterdata/master-registry",
            element: <MasterDataRegistry />,
          },
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
            path: "/masterdata/listing-category",
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
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Duplicate Data",
            path: "/masterdata/duplicate-data",
            element: <DuplicateData />,
          }
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
            name: "AskLaila Data",
            path: "listing-master-data/asklaila-data",
            element: <AsklailaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "ATM Data",
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
            name: "College Dunia Data",
            path: "listing-master-data/college-dunia-data",
            element: <CollegeDuniaData />,
          }, 
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Duplicate Data",
            path: "listing-master-data/duplicate-data",
            element: <DuplicateData />,
          }, 
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Google Data",
            path: "listing-master-data/google-data",
            element: <GoogleData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Google Map Data",
            path: "listing-master-data/google-map-data",
            element: <GoogleMapData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Hey Places Data",
            path: "listing-master-data/hey-places-data",
            element: <HeyPlacesData />,
          }, 
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Just Dial Data",
            path: "listing-master-data/just-dial-data",
            element: <JustDialData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Magic Pin Data",
            path: "listing-master-data/magic-pin-data",
            element: <MagicPinData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Near Buy Data",
            path: "listing-master-data/near-buy-data",
            element: <NearBuyData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Pinda Data",
            path: "listing-master-data/pinda-data",
            element: <PindaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "PO India Data",
            path: "listing-master-data/po-india-data",
            element: <POIndiaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Schoolgis Data",
            path: "listing-master-data/schoolgis-data",
            element: <SchoolgisData />,
          }, 
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Shiksha Data",
            path: "listing-master-data/shiksha-data",
            element: <ShikshaData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Yellow Pages Data",
            path: "listing-master-data/yellow-pages-data",
            element: <YellowPagesData />,
          },
          // ... rest of listing data
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
            icon: <TableCellsIcon {...icon} />,
            name: "Amazon Data",
            path: "product-master-data/amazon-data",
            element: <AmazonData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "BigBasket Data",
            path: "product-master-data/bigbasket-data",
            element: <BigBasketData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "BlinkIt Data",
            path: "product-master-data/blinkit-data",
            element: <BlinkIt />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "D-Mart Data",
            path: "product-master-data/d-mart-data",
            element: <DmartData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Flipkart Data",
            path: "product-master-data/flipkart-data",
            element: <FlipkartData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "India Mart Data",
            path: "listing-master-data/india-mart-data",
            element: <IndiaMart />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "JioMart Data",
            path: "product-master-data/jiomart-data",
            element: <JioMartData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Zepto Data",
            path: "product-master-data/zepto-data",
            element: <ZeptoData />,
          },
          {
            icon: <TableCellsIcon {...icon} />,
            name: "Zomato Data",
            path: "product-master-data/zomato-data",
            element: <ZomatoData />,
          },
          {
            icon: <XCircleIcon {...icon} />,
            name: "Incomplete Data",
            path: "product-master-data/incomplete-data",
            element: <ProductIncomplate />,
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
          // ... rest of scrappers
          {
            icon: <ShoppingCartIcon {...icon} />,
            name: "India Mart",
            path: "/scrapper/indiamart",
            element: <IndiamartScrapper />,
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