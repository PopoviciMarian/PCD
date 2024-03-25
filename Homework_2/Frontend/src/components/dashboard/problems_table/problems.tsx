'use client';

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
import { ArrowRight as ArrowRightIcon } from '@phosphor-icons/react/dist/ssr/ArrowRight';
import dayjs from 'dayjs';
import Link from 'next/link';
export type TProblem = {
    id: string;
    name: string;
    description: string;
    author: string;
    solutions: [string];
    tests: [string];
}

export const ProblemsTable = ({ problems = [] }: { problems?: TProblem[] }): React.JSX.Element => {
    return (
        <Card>
            <CardHeader title="Problems" />
            <Divider />
            <Box sx={{ overflowX: 'auto' }}>
                <Table sx={{ minWidth: 800 }}>
                    <TableHead>
                        <TableRow>
                            <TableCell>Problem</TableCell>
                            <TableCell>Author</TableCell>
                            {/* <TableCell>Total Solutions</TableCell> */}
                            <TableCell>Tests</TableCell>
                            <TableCell align='right' />
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {problems.map((problem, index) => {
                            return (
                                <TableRow hover key={index} >
                                    <TableCell>{problem?.name}</TableCell>
                                    <TableCell>{problem?.author}</TableCell>
                                    {/* <TableCell>{problem?.solutions?.length}</TableCell> */}
                                    <TableCell>{problem?.tests?.length}</TableCell>
                                    <TableCell align='right'>
                                        <Link href={`/dashboard/problem?id=${problem?.id}`}>
                                            <Button size="small" variant="text">
                                                View
                                            </Button>
                                        </Link>
                                    </TableCell>
                                </TableRow>
                            );
                        })}
                    </TableBody>
                </Table>
            </Box>
            <CardActions>
                <Button endIcon={<ArrowRightIcon />} size="small" variant="text">
                    Add Problem

                </Button>
            </CardActions>
        </Card>
    );
}
