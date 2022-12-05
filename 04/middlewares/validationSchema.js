export const validationSchema = (reqField, schema) => (req, res, next) => {
  const { value, error } = schema.validate(req[reqField], { abortEarly: false });

  if (error) {
    res.status(400).json({ errors: error.details.map(d => d.message) });
  } else {
    req[reqField] = value;
    next();
  }
}
