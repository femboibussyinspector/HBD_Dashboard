import {
  Card,
  CardHeader,
  CardBody,
  Typography,
} from "@material-tailwind/react";
import PropTypes from "prop-types";

export function StatisticsCard({ color, icon, title, value, footer }) {
  return (
    <Card className="relative overflow-hidden border border-white/40 bg-white/70 shadow-lg backdrop-blur-xl hover:scale-105 transition-transform duration-300">
      <div className="absolute top-0 right-0 -mr-4 -mt-4 h-24 w-24 rounded-full bg-blue-gray-50/50 blur-2xl" />
      
      <CardHeader
        variant="gradient"
        color={color}
        floated={false}
        shadow={false}
        className="absolute grid h-12 w-12 place-items-center rounded-xl"
      >
        {icon}
      </CardHeader>
      <CardBody className="p-4 text-right z-10 relative">
        <Typography variant="small" className="font-bold text-blue-gray-600 uppercase tracking-widest text-[10px]">
          {title}
        </Typography>
        <Typography variant="h3" color="blue-gray" className="mt-1">
          {value}
        </Typography>
      </CardBody>
      {footer && (
        <CardBody className="border-t border-blue-gray-50/50 p-4">
          {footer}
        </CardBody>
      )}
    </Card>
  );
}

StatisticsCard.defaultProps = {
  color: "blue",
  footer: null,
};

StatisticsCard.propTypes = {
  color: PropTypes.oneOf([
    "white",
    "blue-gray",
    "gray",
    "brown",
    "deep-orange",
    "orange",
    "amber",
    "yellow",
    "lime",
    "light-green",
    "green",
    "teal",
    "cyan",
    "light-blue",
    "blue",
    "indigo",
    "deep-purple",
    "purple",
    "pink",
    "red",
  ]),
  icon: PropTypes.node.isRequired,
  title: PropTypes.node.isRequired,
  value: PropTypes.node.isRequired,
  footer: PropTypes.node,
};

export default StatisticsCard;