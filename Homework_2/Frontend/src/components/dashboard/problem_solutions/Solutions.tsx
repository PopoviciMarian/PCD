import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardHeader from '@mui/material/CardHeader';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import type { SxProps } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import dayjs from 'dayjs';

import { collection, getDocs, doc, Firestore } from 'firebase/firestore';
import { db } from '../../../config/firestore';
import { useCollectionData } from 'react-firebase-hooks/firestore';
import Result from './Result';
import { IconButton, Tooltip } from '@mui/material';
import { Code } from '@phosphor-icons/react/dist/ssr';


const statusMap = {
    pending: { label: 'Pending', color: 'warning' },
    compiling: { label: 'Compiling', color: 'info' },
    compiled: { label: 'Compiled', color: 'info' },
    executing: { label: 'Executing', color: 'info' },
    executed: { label: 'Executed', color: 'info' },
    error: { label: 'Error', color: 'error' },
    'error compiling': { label: 'Error Compiling', color: 'error' },

} as const;


type TResult = {

    solution_id: string;
    status: 'Passed' | 'Failed';
    test_id: string;
    time: number;
}

type TSolution = {
    code: string;
    id: string;
    author: string;
    status: 'pending' | 'compiling' | 'compiled' | 'executing' | 'executed' | 'error';
    problem: string;
    results: TResult[];
    createdAt: any;
}


const Solutions = ({ problemId }: { problemId: string }): React.JSX.Element => {
    const solutionsRef = db.collection('solutions');
    const docRef = doc(db, 'problems', problemId);
    const query: any = solutionsRef.where('problem', '==', docRef);
    const [solutions] = useCollectionData<TSolution>(query);


    if (!solutions) return <div></div>;
    const sortedSolutions = solutions.sort((a, b) => {
        return b?.createdAt?.toDate()?.getTime() - a?.createdAt?.toDate()?.getTime();
    });

    return (
        <Box>
            <Card>
                <CardHeader title="Solutions" />
                <Divider />
                <Box sx={{ overflowX: 'auto' }}>
                    <Table sx={{ minWidth: 800 }}>
                        <TableHead>
                            <TableRow>

                                <TableCell />
                                <TableCell>CreatedAt</TableCell>
                                <TableCell>Author</TableCell>
                                <TableCell>Status</TableCell>
                                <TableCell>Results</TableCell>

                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {sortedSolutions.map((solution, index) => {
                                return (
                                    <TableRow hover key={index} >
                                        <TableCell>
                                            {/*tooltip with the code*/}
                                            <Tooltip title={<TooltipCode code={solution.code} />} placement="left">
                                                <Code />
                                            </Tooltip>

                                        </TableCell>
                                        <TableCell>{solution?.createdAt?.toDate()?.toLocaleString()}
                                        </TableCell>
                                        <TableCell>{solution.author}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={statusMap[solution.status].label}
                                                color={statusMap[solution.status].color}
                                            />
                                        </TableCell>
                                        <TableCell>
                                            {solution?.results?.map((result, index) => {
                                                return (
                                                    <Result key={index} index={index} refResult={result} />
                                                )
                                            }
                                            )}
                                        </TableCell>

                                    </TableRow>
                                )
                            })}
                        </TableBody>
                    </Table>
                </Box>
            </Card>


        </Box>
    );
}

import Editor from '@monaco-editor/react';
const TooltipCode = ({ code }: { code: string }) => {
    return (
        <div>

            <Editor

                width="500px"
                height="300px"
                defaultLanguage="cpp"
                defaultValue={code}
                theme="vs-dark"
                options={{ readOnly: true }}
                // don't show the minimap
                onMount={(editor, monaco) => {
                    editor.updateOptions({ minimap: { enabled: false } });
                }}
            />
        </div>



    );
}

export default Solutions;