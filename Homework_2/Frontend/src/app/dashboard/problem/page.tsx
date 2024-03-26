'use client';

import * as React from 'react';
import { useSearchParams } from 'next/navigation'
import { collection, getDocs } from 'firebase/firestore';
import { db } from '../../../config/firestore';
import { TProblem } from '@/components/dashboard/problems_table/problems';
import SolutionEditor from '@/components/dashboard/problem_solution/solutionEditor';
import Solutions from '@/components/dashboard/problem_solutions/Solutions';
import Markdown from 'react-markdown'
import { Box } from '@mui/material';

const ProblemPage = () => {
    const [problem, setProblem] = React.useState<TProblem | null>(null);

    const getProblemById = async (id: string) => {
        const problemCol = collection(db, 'problems');
        const problemSnapshot = await getDocs(problemCol);
        const problemList = problemSnapshot.docs.map(doc => { return { ...doc.data(), id: doc.id } });
        const problem = problemList.find(problem => problem.id === id);
        setProblem(problem as any);
    }

    const searchParams = useSearchParams();
    const id = searchParams.get('id');
    React.useEffect(() => {
        getProblemById(id as string);
    }, [id]);

    return (
        <div>
            {problem &&
                <div>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                        <h1>{problem.name}</h1>
                        <h3>{problem.author}</h3>
                    </Box>
                    <Markdown>{problem.description}</Markdown>
                </div>

            }
            <SolutionEditor problemId={id as string} />
            <Solutions problemId={id as string} />
        </div>
    );

}

export default ProblemPage;
