'use client';
import { Box, Chip, Typography } from "@mui/material"
import { useDocumentData } from 'react-firebase-hooks/firestore';
import { db } from '../../../config/firestore';
import { doc } from "firebase/firestore";


type TResult = {
    solution_id: string;
    status: 'Passed' | 'Failed' | 'T'
    test_id: string;
    time: number;
}

const Result = ({ index, refResult }: { index: number, refResult: any }) => {
    const [result] = useDocumentData<TResult>(refResult);
    if (!result) return <div></div>;


    return (
        <Box sx={{ mb: 1, display: 'flex', flexDirection: 'row', alignItems: 'center', border: '1px solid #d3d3d3', borderRadius: '5px', p: 2, justifyContent: 'space-between' }}>
            <Typography variant="h6">Test {index + 1}</Typography>
            <Chip sx={{ p: 0, mx: 3 }} label={result.status} color={result.status === 'Passed' ? 'success' : 'error'} />

            <Typography>{result.time.toFixed(4)} ms</Typography>
        </Box>
    );

}

export default Result;