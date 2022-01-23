const dotenv = require("dotenv");

dotenv.config();

module.exports = {
  plugins: {
    "posthtml-expressions": {
      locals: {
        MAPPINGS_URL: process.env.MAPPINGS_URL
      }
    }
  }
};
