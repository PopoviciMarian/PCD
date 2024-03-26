
'use client';

import React from 'react';
import Editor from '@monaco-editor/react';
import { Box, Button } from '@mui/material';
import { collection, getDocs, addDoc, doc } from 'firebase/firestore';
import { db } from '../../../config/firestore';
import firebase from 'firebase/compat/app'
import { useUser } from '../../../hooks/use-user';

const SolutionEditor = ({ problemId }: { problemId: string }) => {
    const { user } = useUser();
    const editorRef = React.useRef<any>(null);
    const handleEditorDidMount = (editor: any, monaco: any) => {
        editorRef.current = editor;
    }
    const defaultValue = `#include <iostream>\n#include <fstream>\n\nusing namespace std;\n\nifstream fin("input.txt");\nofstream fout("output.txt");\n\nint main() {\n\n //write your code here, reed the input from input.txt and write the output to output.txt if needed\n\nreturn 0;\n}`;

    const submitSolution = async () => {
        const code = editorRef.current.getValue();


        const problemRef = db.collection('problems').doc(problemId);
        db.collection('solutions').add({
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            code: code, problem: problemRef, status: 'pending', author: user?.email
        });

        //     addDoc(col, { code: code, problem: problemRef });
    }

    return (
        <Box>
            <Box sx={{ width: '100%', border: '3px solid #d3d3d3', borderRadius: '5px' }}>
                <Editor
                    height="400px"
                    defaultLanguage="cpp"


                    defaultValue={defaultValue}
                    onMount={handleEditorDidMount}
                    theme="vs-dark"

                />

            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', padding: '10px' }}>

                <Button variant="contained" color="primary" sx={{ marginRight: '10px', ml: 2 }} onClick={submitSolution}>Submit</Button>

            </Box>
        </Box>
    );

}

export default SolutionEditor; 