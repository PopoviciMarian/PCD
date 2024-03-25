'use client';

import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import { collection, getDocs } from 'firebase/firestore';
import { db } from '../../config/firestore';


import { TProblem, ProblemsTable } from '../../components/dashboard/problems_table/problems';

const Dashboard = () => {

    const [problems, setProblems] = React.useState([]);


    const getProblems = async () => {
        const problemsCol = collection(db, 'problems');
        const problemsSnapshot = await getDocs(problemsCol);
        const problemsList = problemsSnapshot.docs.map(doc => { return { ...doc.data(), id: doc.id } });
        setProblems(problemsList as any);
    }

    React.useEffect(() => {
        getProblems();
    }, []);

    // for the problems will be a table with the name, description, author and number of solutions

    return (
        <div>
            {problems.length > 0 &&
                <ProblemsTable problems={problems as TProblem[]} />
            }

        </div>
    );

}


export default Dashboard;
