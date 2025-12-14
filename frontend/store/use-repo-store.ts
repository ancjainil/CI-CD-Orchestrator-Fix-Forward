import { create } from "zustand";

type State = {
  repo: string | null;
  setRepo: (repo: string) => void;
};

export const useRepoStore = create<State>((set) => ({
  repo: null,
  setRepo: (repo) => set({ repo }),
}));
