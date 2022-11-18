export const isGitRepo = (url) => {
  return url.startsWith("https:") && url.endsWith(".git");
};
