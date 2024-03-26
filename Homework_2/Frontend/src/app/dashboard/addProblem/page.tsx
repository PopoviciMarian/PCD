'use client';
import { Button, Card, CardActions, CardContent, CardHeader, Divider, FormControl, Grid, Icon, InputLabel, OutlinedInput, Stack, Typography } from "@mui/material";
import React from "react";
import MDEditor, { commands } from '@uiw/react-md-editor';
import IconButton from '@mui/material/IconButton';
import { Trash } from "@phosphor-icons/react";
import { useUser } from "@/hooks/use-user";
import { collection, getDocs } from 'firebase/firestore';
import { db } from '../../../config/firestore';
import { useRouter } from 'next/navigation'
type TTest = {
    input: string;
    output: string;
    timeLimit: number;
}

const AddProblemPage = () => {
    const [name, setName] = React.useState<string | undefined>('');
    const [value, setValue] = React.useState<string | undefined>('Write problem description here');
    const [tests, setTests] = React.useState<TTest[]>([{ input: '', output: '', timeLimit: 10 }]);
    const { user } = useUser();
    const router = useRouter()
    const addTest = () => {
        setTests([...tests, { input: '', output: '', timeLimit: 10 }]);
    }
    const removeTest = (index: number) => {
        const newTests = tests.filter((_, i) => i !== index);
        setTests(newTests);
    }

    const handleTestChange = (index: number, key: string, value: string) => {
        const newTests = tests.map((test, i) => {
            if (i === index) {
                return { ...test, [key]: value }
            }
            return test;
        });
        setTests(newTests);
    }

    const handleSave = async () => {


        const testsData = tests.map(test => {
            return {
                input: test.input,
                output: test.output,
                timeout: test.timeLimit
            }
        })
        const ids = [];
        for (let i = 0; i < testsData.length; i++) {
            const test = testsData[i];
            const refTest = await db.collection('tests').add(test);
            ids.push(refTest);
        }

        const problemData = {
            author: user?.email,
            description: value,
            name: name,
            tests: ids
        }

        const problem = await db.collection('problems').add(problemData);
        // print problem id 
        router.push('/dashboard/problem?id=' + problem.id);





    }

    return (
        <Stack spacing={3}>
            <Card>
                <CardHeader title="Add Problem" />
                <Divider />
                <CardContent>
                    <Grid container spacing={3}>
                        <Grid md={12} xs={12}>
                            <FormControl sx={{ mx: 2, mb: 3, width: "50%" }} required>
                                <InputLabel>Problem Name</InputLabel>
                                <OutlinedInput label="Problem Name" name="problemName" value={name} onChange={(e) => setName(e.target.value)} />
                            </FormControl>
                        </Grid>
                        <Grid sx={{ ml: 3, mb: 4 }} md={12} xs={12}>
                            <div className="container" data-color-mode="light">
                                <MDEditor
                                    value={value}
                                    preview="edit"
                                    onChange={setValue}

                                    components={{
                                        toolbar: (command, disabled, executeCommand) => {
                                            if (command.keyCommand === 'code') {
                                                return (
                                                    <button
                                                        aria-label="Insert code"
                                                        disabled={disabled}
                                                        onClick={(evn) => {
                                                            evn.stopPropagation();
                                                            executeCommand(command, command.groupName)
                                                        }}
                                                    >
                                                        Code
                                                    </button>
                                                )
                                            }
                                        }
                                    }}
                                />
                            </div>
                        </Grid>
                        <Divider />
                        <Typography variant="h6" sx={{ ml: 2, mt: 2, mb: 2 }}>Tests</Typography>


                        <Grid md={12} xs={12}>
                            {tests.map((test, index) => (
                                <Grid gap={3} md={12} xs={12} sx={{ ml: 2, display: 'flex', flexDirection: 'row' }}>
                                    <FormControl fullWidth required>
                                        <InputLabel>input.txt</InputLabel>
                                        <OutlinedInput label="Tests" name="tests" value={test.input} onChange={(e) => handleTestChange(index, 'input', e.target.value)} />
                                    </FormControl>
                                    <FormControl fullWidth required>
                                        <InputLabel>output.txt</InputLabel>
                                        <OutlinedInput label="Tests" name="tests" value={test.output} onChange={(e) => handleTestChange(index, 'output', e.target.value)} />
                                    </FormControl>
                                    <FormControl sx={{ mb: 3, width: "50%" }} required>
                                        <InputLabel>Time Limit</InputLabel>
                                        <OutlinedInput type="number" label="Time Limit" name="timeLimit" value={test.timeLimit} onChange={(e) => handleTestChange(index, 'timeLimit', e.target.value)} />
                                    </FormControl>
                                    <IconButton aria-label="delete"
                                        sx={{ mb: 2 }}
                                        onClick={() => removeTest(index)}
                                    >
                                        <Trash />
                                    </IconButton>

                                </Grid>
                            ))}

                        </Grid>
                        <Grid md={12} xs={12} sx={{ ml: 2, display: 'flex', flexDirection: 'row', justifyContent: 'flex-end' }}>
                            <Button variant="contained"
                                onClick={addTest}
                            >Add Test</Button>
                        </Grid>
                    </Grid>

                </CardContent>
                <Divider />
                <CardActions sx={{ justifyContent: 'flex-end' }}>
                    <Button variant="contained" onClick={handleSave}>Save problem</Button>
                </CardActions>
            </Card>

        </Stack >
    )
}



export default AddProblemPage;