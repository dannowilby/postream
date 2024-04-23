
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';

// todo: create the posts type
// todo: create the files typs

export async function load({ params }) {

  const sql = postgres(`postgresql://${process.env.POSTGRES_USER}:${process.env.POSTGRES_PASSWORD}@${process.env.POSTGRES_HOST}:${process.env.POSTGRES_PORT}/${process.env.POSTGRES_DB}`);

  const posts = await sql`select title, url, tags, post_type, post_time from posts;`

  return posts;
}

export const prerender = true;
