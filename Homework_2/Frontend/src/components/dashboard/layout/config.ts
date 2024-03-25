import type { NavItemConfig } from '@/types/nav';
import { paths } from '@/paths';

export const navItems = [
  { key: 'overview', title: 'Problems', href: paths.dashboard.overview, icon: 'problems' },
  { key: 'create', title: 'Add Problem', href: paths.dashboard.addProblem, icon: 'create' },
  // { key: 'profile', title: 'Profile', href: paths.dashboard.account, icon: 'profile' },
  // { key: 'logout', title: 'Logout', href: paths.dashboard.account, icon: 'logout' },

] satisfies NavItemConfig[];
