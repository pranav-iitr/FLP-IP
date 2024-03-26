module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: ["google", "plugin:react/recommended"],
  overrides: [
    {
      env: {
        node: true,
      },
      files: [".eslintrc.{js,cjs}"],
      parserOptions: {
        sourceType: "script",
      },
    },
  ],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react"],
  rules: {
    "linebreak-style": 0,
    indent: 0,
    quotes: 0,
    "object-curly-spacing": 0,
    "react/react-in-jsx-scope": 0,
    "react/prop-types": 0,
    "max-len": 0,
    "react/jsx-key": 0,
    "react/no-unknown-property": 0,
    "require-jsdoc": 0,
    "new-cap": 0,
  },
};
