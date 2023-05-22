CREATE OR REPLACE FUNCTION notify_changes()
RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('changes', ''); -- отправка уведомления
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_notify_changes
AFTER INSERT OR DELETE OR UPDATE ON email_message -- название таблицы, изменения в которой необходимо отслеживать
FOR EACH ROW EXECUTE PROCEDURE notify_changes();