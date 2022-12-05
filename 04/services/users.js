const users = {};

export const addUser = ({ Id, Name, Email }) => users[Id] = { Id, Name, Email };

export const removeUser = ({ Id }) => {
  if (!(Id in users)) {
    return false;
  }

  delete users[Id];

  return true;
}

export const getUser = ({ Id }) => users[Id] ?? null;

export const queryUsers = ({ Name, Email }) => {
  const cleanName = Name?.toLowerCase() ?? null;
  const cleanEmail = Email?.toLowerCase() ?? null;

  return Object.values(users)
    .filter(user =>
      (Name && user.Name.toLowerCase() === cleanName) ||
      (Email && user.Email.toLowerCase() === cleanEmail)
    );
}
