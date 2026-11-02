export type Document = {id:string;name:string;size:number;pages:number;chunks:number};
export type Citation = {document_id:string;document_name:string;page:number;excerpt:string};
export type Message = {role:'user'|'assistant';content:string;citations?:Citation[]};
