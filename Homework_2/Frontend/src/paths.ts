export const paths = {
  home: '/',
  auth: { signIn: '/auth/sign-in', signUp: '/auth/sign-up', resetPassword: '/auth/reset-password' },
  dashboard: {
    overview: '/dashboard',
    addProblem: '/dashboard/addProblem',
    problem: '/dashboard/problem',
  },
  errors: { notFound: '/errors/not-found' },
} as const;
